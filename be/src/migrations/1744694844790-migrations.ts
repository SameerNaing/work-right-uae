import { MigrationInterface, QueryRunner } from "typeorm";

export class Migrations1744694844790 implements MigrationInterface {
    name = 'Migrations1744694844790'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "conversations" ("createdByUserId" uuid, "updatedByUserId" uuid, "deletedByUserId" uuid, "id" uuid NOT NULL DEFAULT uuid_generate_v4(), "name" character varying(500) NOT NULL DEFAULT 'New Chat', CONSTRAINT "PK_ee34f4f7ced4ec8681f26bf04ef" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "messages" ("createdByUserId" uuid, "updatedByUserId" uuid, "deletedByUserId" uuid, "id" uuid NOT NULL DEFAULT uuid_generate_v4(), "content" text NOT NULL, "feedback" "public"."messages_feedback_enum", "role" "public"."messages_role_enum" NOT NULL, "senderId" character varying(255) NOT NULL, "conversationId" uuid NOT NULL, "parentMessageId" uuid, CONSTRAINT "REL_379d3b2679ddf515e5a90de015" UNIQUE ("parentMessageId"), CONSTRAINT "PK_18325f38ae6de43878487eff986" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "users" ("createdByUserId" uuid, "updatedByUserId" uuid, "deletedByUserId" uuid, "id" uuid NOT NULL DEFAULT uuid_generate_v4(), "name" character varying(255) NOT NULL, "email" character varying(255) NOT NULL, CONSTRAINT "PK_a3ffb1c0c8416b9fc6f907b7433" PRIMARY KEY ("id"))`);
        await queryRunner.query(`ALTER TABLE "conversations" ALTER COLUMN "name" DROP DEFAULT`);
        await queryRunner.query(`ALTER TABLE "conversations" ADD CONSTRAINT "FK_775d68d034ed55622ec1d3930ac" FOREIGN KEY ("createdByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "conversations" ADD CONSTRAINT "FK_28f69acd7960ce8852beb2e8b6e" FOREIGN KEY ("updatedByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "conversations" ADD CONSTRAINT "FK_029f37876043fa2fb35e11a831a" FOREIGN KEY ("deletedByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "messages" ADD CONSTRAINT "FK_8a1c3a401480e24b6f0524cd9ba" FOREIGN KEY ("createdByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "messages" ADD CONSTRAINT "FK_72941f3d4b2ff1c8a5a74e8adf9" FOREIGN KEY ("updatedByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "messages" ADD CONSTRAINT "FK_3faa510747cd1817d2160dadca6" FOREIGN KEY ("deletedByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "messages" ADD CONSTRAINT "FK_379d3b2679ddf515e5a90de0153" FOREIGN KEY ("parentMessageId") REFERENCES "messages"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "messages" ADD CONSTRAINT "FK_e5663ce0c730b2de83445e2fd19" FOREIGN KEY ("conversationId") REFERENCES "conversations"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "users" ADD CONSTRAINT "FK_07bdef65006aa4bc8950f70e213" FOREIGN KEY ("createdByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "users" ADD CONSTRAINT "FK_30518ee912316676e8cebd9cca0" FOREIGN KEY ("updatedByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
        await queryRunner.query(`ALTER TABLE "users" ADD CONSTRAINT "FK_4ffb8c41fed6d32b356ae4709cb" FOREIGN KEY ("deletedByUserId") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "users" DROP CONSTRAINT "FK_4ffb8c41fed6d32b356ae4709cb"`);
        await queryRunner.query(`ALTER TABLE "users" DROP CONSTRAINT "FK_30518ee912316676e8cebd9cca0"`);
        await queryRunner.query(`ALTER TABLE "users" DROP CONSTRAINT "FK_07bdef65006aa4bc8950f70e213"`);
        await queryRunner.query(`ALTER TABLE "messages" DROP CONSTRAINT "FK_e5663ce0c730b2de83445e2fd19"`);
        await queryRunner.query(`ALTER TABLE "messages" DROP CONSTRAINT "FK_379d3b2679ddf515e5a90de0153"`);
        await queryRunner.query(`ALTER TABLE "messages" DROP CONSTRAINT "FK_3faa510747cd1817d2160dadca6"`);
        await queryRunner.query(`ALTER TABLE "messages" DROP CONSTRAINT "FK_72941f3d4b2ff1c8a5a74e8adf9"`);
        await queryRunner.query(`ALTER TABLE "messages" DROP CONSTRAINT "FK_8a1c3a401480e24b6f0524cd9ba"`);
        await queryRunner.query(`ALTER TABLE "conversations" DROP CONSTRAINT "FK_029f37876043fa2fb35e11a831a"`);
        await queryRunner.query(`ALTER TABLE "conversations" DROP CONSTRAINT "FK_28f69acd7960ce8852beb2e8b6e"`);
        await queryRunner.query(`ALTER TABLE "conversations" DROP CONSTRAINT "FK_775d68d034ed55622ec1d3930ac"`);
        await queryRunner.query(`ALTER TABLE "conversations" ALTER COLUMN "name" SET DEFAULT 'New Chat'`);
        await queryRunner.query(`DROP TABLE "users"`);
        await queryRunner.query(`DROP TABLE "messages"`);
        await queryRunner.query(`DROP TABLE "conversations"`);
    }

}
