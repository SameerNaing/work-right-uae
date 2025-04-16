import { Column, Entity, OneToMany, PrimaryGeneratedColumn } from 'typeorm';

import { BaseEntity } from '../base-entity';
import { MessageEntity } from './message.entity';

@Entity('conversations')
export class ConversationEntity extends BaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'varchar', length: 500, default: 'New Chat' })
  name: string;

  @OneToMany(() => MessageEntity, (message) => message.conversation)
  messages: MessageEntity[];
}
