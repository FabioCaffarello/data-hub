import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

import { ApiFeatureConfigModule } from '@data-hub/sd-nest/feature-config';
import { ApiFeatureIngestorConfigModule } from '@data-hub/sd-nest/features/ingestor-config';
import { MongoConfiguration, mongoConfiguration } from '@data-hub/sd-nest/utils-config';

@Module({
  imports: [
    ApiFeatureConfigModule,
    ApiFeatureIngestorConfigModule,
    MongooseModule.forRootAsync({
      inject: [
        mongoConfiguration.KEY
      ],
      useFactory: (config: MongoConfiguration) => {
        return {
          uri: config.uri,
          dbName: config.dbName,
        };
      }
    })
  ],
  controllers: [],
})
export class AppModule {}
