import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { UserEntity } from 'src/database/auth/user.entity';
import { FindOptionsRelations, FindOptionsSelect, Repository } from 'typeorm';
import { UpdateUserRequestDto } from './DTOs';

@Injectable()
export class UserService {
  private readonly logger = new Logger(UserService.name);
  constructor(
    @InjectRepository(UserEntity)
    private readonly userRepository: Repository<UserEntity>,
  ) {}

  async findById(
    id: string,
    {
      select = {},
      relations,
      throwError = true,
    }: {
      select?: FindOptionsSelect<UserEntity>;
      relations?: FindOptionsRelations<UserEntity>;
      throwError?: boolean;
    },
  ) {
    const user = await this.userRepository.findOne({
      where: { id },
      select,
      relations,
    });

    if (!user && throwError) {
      this.logger.error({
        message: `User with id ${id} not found`,
        id,
      });
      throw new NotFoundException(`User with id ${id} not found`);
    }

    return user;
  }

  async findByEmail(
    email: string,
    {
      select = {},
      withDeleted = false,
      relations,
      throwError = true,
    }: {
      select?: FindOptionsSelect<UserEntity>;
      withDeleted?: boolean;
      relations?: FindOptionsRelations<UserEntity>;
      throwError?: boolean;
    },
  ) {
    const user = await this.userRepository.findOne({
      where: { email },
      withDeleted,
      select,
      relations,
    });

    if (!user && throwError) {
      this.logger.error({
        message: `User with email ${email} not found`,
        email,
      });
      throw new NotFoundException(`User with email ${email} not found`);
    }

    return user;
  }

  async createUser(data: Partial<UserEntity>) {
    const user = this.userRepository.create(data);
    return await this.userRepository.save(user);
  }

  async restoreUser(id: string) {
    await this.userRepository.update(
      { id },
      { deletedAt: null as any, deletedBy: null as any },
    );

    return;
  }

  async deleteUser(id: string, operationUserId?: string) {
    await this.userRepository.update(
      { id },
      {
        deletedAt: new Date(),
        deletedBy: { id: operationUserId || id } as any,
      },
    );
  }

  async updateUser(id: string, data: UpdateUserRequestDto) {
    await this.userRepository.update(
      { id },
      {
        name: data.name,
      },
    );
    return;
  }
}
