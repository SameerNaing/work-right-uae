import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { RedisModule } from '@nestjs-modules/ioredis';

import { environment } from './config/environment';
import typeorm from './config/typeorm';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UserModule } from './core/user/user.module';
import { AuditSubscriber } from './subscribers/audit.subscriber';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [typeorm],
    }),
    RedisModule.forRoot({
      type: environment.redis.type as any,
      url: environment.redis.url,
    }),
    TypeOrmModule.forRootAsync({
      inject: [ConfigService],
      // @ts-expect-error
      useFactory: async (configService: ConfigService) => {
        return configService.get('typeorm');
      },
    }),
    UserModule,
  ],

  controllers: [AppController],
  providers: [AppService, AuditSubscriber],
})
export class AppModule {}
