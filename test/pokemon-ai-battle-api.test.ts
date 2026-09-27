import * as cdk from 'aws-cdk-lib/core';
import { Match, Template } from 'aws-cdk-lib/assertions';
import { PokemonAiBattleApiStack } from '../lib/pokemon-ai-battle-api-stack';

// Skip Docker bundling of the Python Lambdas so these tests stay fast and don't need Docker.
const synth = () => {
  const app = new cdk.App({ context: { 'aws:cdk:bundling-stacks': [] } });
  return Template.fromStack(new PokemonAiBattleApiStack(app, 'TestStack'));
};

describe('PokemonAiBattleApiStack', () => {
  const template = synth();

  test('GET /health is served by the Python health Lambda behind the authorizer', () => {
    template.hasResourceProperties('AWS::ApiGateway::Resource', { PathPart: 'health' });
    template.hasResourceProperties('AWS::ApiGateway::Method', {
      HttpMethod: 'GET',
      AuthorizationType: 'CUSTOM',
      AuthorizerId: Match.anyValue(),
    });
    template.hasResourceProperties('AWS::Lambda::Function', {
      FunctionName: 'pokemon-battle-health',
      Runtime: 'python3.14',
      Handler: 'pokemon_battle.handlers.health.handler',
    });
  });

  test('every non-preflight method requires the authorizer', () => {
    const methods = template.findResources('AWS::ApiGateway::Method');
    for (const method of Object.values(methods)) {
      const { HttpMethod, AuthorizationType } = method.Properties;
      // Browsers send CORS preflights without an Authorization header, so they must stay open.
      expect(AuthorizationType).toBe(HttpMethod === 'OPTIONS' ? 'NONE' : 'CUSTOM');
    }
  });

  test('the authorizer checks the Authorization header and caches its decision for 5 minutes', () => {
    template.hasResourceProperties('AWS::ApiGateway::Authorizer', {
      Type: 'TOKEN',
      IdentitySource: 'method.request.header.Authorization',
      AuthorizerResultTtlInSeconds: 300,
    });
    template.hasResourceProperties('AWS::Lambda::Function', {
      FunctionName: 'pokemon-battle-authorizer',
      Runtime: 'python3.14',
      Handler: 'pokemon_battle.handlers.authorizer.handler',
      Environment: { Variables: { SHARED_SECRET_ARN: Match.anyValue() } },
    });
  });

  test('the shared secret is generated in Secrets Manager and readable by the authorizer', () => {
    template.hasResourceProperties('AWS::SecretsManager::Secret', {
      Name: '/pokemon-ai-battle/api-shared-secret',
      GenerateSecretString: Match.objectLike({ PasswordLength: 48 }),
    });
    template.hasResourceProperties('AWS::IAM::Policy', {
      PolicyDocument: {
        Statement: Match.arrayWith([
          Match.objectLike({
            Action: Match.arrayWith(['secretsmanager:GetSecretValue']),
            Effect: 'Allow',
          }),
        ]),
      },
    });
  });

  test('API Gateway error responses carry CORS headers so browsers can see 401s', () => {
    for (const type of ['DEFAULT_4XX', 'DEFAULT_5XX']) {
      template.hasResourceProperties('AWS::ApiGateway::GatewayResponse', {
        ResponseType: type,
        ResponseParameters: {
          'gatewayresponse.header.Access-Control-Allow-Origin': "'*'",
        },
      });
    }
  });
});
