import { ApiResponseProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

@Expose()
export class UserMeResponseDto {
  @ApiResponseProperty()
  @Expose()
  id: string;

  @ApiResponseProperty()
  @Expose()
  email: string;

  @ApiResponseProperty()
  @Expose()
  name: string;
}
