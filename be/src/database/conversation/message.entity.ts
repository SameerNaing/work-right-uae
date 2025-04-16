import {
  Column,
  Entity,
  JoinColumn,
  ManyToOne,
  OneToOne,
  PrimaryGeneratedColumn,
} from 'typeorm';

import { BaseEntity } from '../base-entity';
import { FeedbackEnum, MessageRole } from 'src/core/conversations/enum';
import { ConversationEntity } from './conversation.entity';

@Entity('messages')
export class MessageEntity extends BaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'text' })
  content: string;

  @Column({ type: 'enum', enum: FeedbackEnum, nullable: true })
  feedback: FeedbackEnum;

  @Column({ type: 'enum', enum: MessageRole })
  role: MessageRole;

  @Column({ type: 'varchar', length: 255 })
  senderId: string;

  @Column({ name: 'conversationId' })
  conversationId: string;

  @Column({ name: 'parentMessageId', nullable: true })
  parentMessageId: string;

  @OneToOne(() => MessageEntity, { nullable: true })
  @JoinColumn({ name: 'parentMessageId' }) // This tells TypeORM which column joins
  parentMessage: MessageEntity;

  @OneToOne(() => MessageEntity, (message) => message.parentMessage)
  childMessage: MessageEntity;

  @ManyToOne(() => ConversationEntity, (conversation) => conversation.messages)
  @JoinColumn({ name: 'conversationId' }) // This tells TypeORM which column joins
  conversation: ConversationEntity;
}
