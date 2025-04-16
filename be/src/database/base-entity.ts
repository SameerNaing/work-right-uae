import {
  Column,
  CreateDateColumn,
  DeleteDateColumn,
  JoinColumn,
  ManyToOne,
  BaseEntity as TypeOrmBaseEntity,
  UpdateDateColumn,
} from 'typeorm';
import { UserEntity } from './auth/user.entity';

export abstract class BaseEntity extends TypeOrmBaseEntity {
  public static userId: string;

  static setUserId(userId: string) {
    this.userId = userId;
  }
  @CreateDateColumn({ type: 'timestamp with time zone' })
  createdAt: Date;

  @UpdateDateColumn({ type: 'timestamp with time zone' })
  updatedAt: Date;

  @DeleteDateColumn({ type: 'timestamp with time zone', nullable: true })
  deletedAt?: Date;

  @Column({ name: 'createdByUserId', nullable: true })
  createdByUserId?: string;

  @Column({ name: 'updatedByUserId', nullable: true })
  updatedByUserId?: string;

  @Column({ name: 'deletedByUserId', nullable: true })
  deletedByUserId?: string;

  @ManyToOne('UserEntity', { nullable: true })
  @JoinColumn({ name: 'createdByUserId' })
  createdBy: UserEntity;

  @ManyToOne('UserEntity', { nullable: true })
  @JoinColumn({ name: 'updatedByUserId' })
  updatedBy: UserEntity;

  @ManyToOne('UserEntity', { nullable: true })
  @JoinColumn({ name: 'deletedByUserId' })
  deletedBy: UserEntity;
}
