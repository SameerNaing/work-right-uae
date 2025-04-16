import { BaseEntity } from 'src/database/base-entity';
import {
  DataSource,
  EntitySubscriberInterface,
  EventSubscriber,
  InsertEvent,
  UpdateEvent,
} from 'typeorm';

@EventSubscriber()
export class AuditSubscriber implements EntitySubscriberInterface {
  constructor(dataSource: DataSource) {
    dataSource.subscribers.push(this);
  }

  beforeInsert(event: InsertEvent<any>) {
    if (event?.entity && BaseEntity.userId) {
      event.entity.createdBy = {
        id: BaseEntity.userId,
      } as any;
    }
  }

  beforeUpdate(event: UpdateEvent<any>) {
    if (event?.entity && BaseEntity.userId) {
      event.entity.updatedBy = {
        id: BaseEntity.userId,
      } as any;
    }
  }
}
