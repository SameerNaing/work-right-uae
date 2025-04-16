/* eslint-disable @typescript-eslint/no-unsafe-call */
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { ValidationPipe, VersioningType } from '@nestjs/common';
import * as bodyParser from 'body-parser';
import * as compression from 'compression';
import { useContainer } from 'class-validator';

import { AppModule } from './app.module';
import { GlobalExceptionHandler } from './filters';
import { environment } from './config/environment';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, { cors: true });

  app.enableVersioning({
    type: VersioningType.URI,
  });

  app.useGlobalFilters(new GlobalExceptionHandler());
  app.useGlobalPipes(
    new ValidationPipe({
      transform: true,
    }),
  );

  if (!environment.isProduction) {
    const config = new DocumentBuilder()
      .setTitle('Work Right UAE Swagger')
      .setDescription('Work Right UAE Backend APIs')
      .setVersion('1.0')
      .addBearerAuth(
        {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          in: 'header',
          name: 'Authorization', // Specifies the custom header name for authorization
        },
        'JWT-Token', // A unique identifier for this specific security definition
      )
      .build();

    const document = SwaggerModule.createDocument(app, config);
    SwaggerModule.setup('api', app, document, {
      swaggerOptions: {
        docExpansion: 'none',
        persistAuthorization: true,
        filter: true,
      },
    });
  }

  app.use(bodyParser.json({ limit: '150mb' }));
  app.use(bodyParser.urlencoded({ limit: '150mb', extended: true }));
  app.use(compression());
  useContainer(app.select(AppModule), { fallbackOnErrors: true });

  await app.listen(environment.port);
}

void bootstrap();
