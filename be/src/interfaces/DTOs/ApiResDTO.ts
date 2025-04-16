import { ApiResponseProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

@Expose()
export class ApiResponseDto<T = any> {
  @Expose()
  @ApiResponseProperty()
  success: boolean;

  @Expose()
  @ApiResponseProperty()
  data: T | any;

  @Expose()
  @ApiResponseProperty()
  message: string;
}
