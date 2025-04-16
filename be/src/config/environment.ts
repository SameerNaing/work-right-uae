import { config as dotenvConfig } from 'dotenv';

dotenvConfig({ path: '.env' });

export const environment = {
  authorization: {
    mlCoreTokenSecret:
      process.env.LLM_SERVER_SECRET || '0e778724c5b64d72b80d11e060c726ee',
    accessTokenSecret:
      process.env.JWT_SECRET || '59ce31e7b63e%476ee8be62c9be7e21220',
    signOptions: {
      expiresIn: '30d',
    },
    sessionExpiryTime: 3 * 30 * 24 * 60 * 60, // 3 months
  },
  redis: {
    type: process.env.REDIS_TYPE || 'single',
    url: process.env.REDIS_URL || 'redis://localhost:6379',
  },
  isProduction: process.env.NODE_ENV === 'production',
  port: +(process.env.PORT || '3002'),
};
