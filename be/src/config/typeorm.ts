import { registerAs } from '@nestjs/config';
import { config as dotenvConfig } from 'dotenv';
import { DataSource, DataSourceOptions } from 'typeorm';

dotenvConfig({ path: '.env' });

const isProduction = process.env.NODE_ENV === 'production';

const config = {
  type: 'postgres',
  host: `${process?.env.DATABASE_HOST || 'localhost'}`,
  port: `${process?.env.DATABASE_PORT || 5432}`,
  username: `${process?.env.DATABASE_USERNAME || 'admin'}`,
  password: `${process?.env.DATABASE_PASSWORD || 'admin'}`,
  database: `${process?.env.DATABASE_NAME || 'work-right-uae'}`,
  autoLoadEntities: true,
  entities: [
    __dirname + '/../**/*.entity{.ts,.js}',
    'dist/**/*.entity{.ts,.js}',
  ],
  migrations: [
    'dist/migrations/*{.ts,.js}',
    __dirname + '/../migrations/*{.ts,.js}',
  ],
  // migrations: ['src/migrations/*.ts'],
  // sync: !isProduction,
  // subscribers: [],
  synchronize: !isProduction,
};

export default registerAs('typeorm', () => config);
export const connectionSource = new DataSource(config as DataSourceOptions);
