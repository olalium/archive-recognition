/*
  Warnings:

  - You are about to alter the column `embedding` on the `Face` table. The data in that column could be lost. The data in that column will be cast from `Decimal(65,30)` to `DoublePrecision`.

*/
-- AlterTable
ALTER TABLE "Face" ALTER COLUMN "embedding" SET DATA TYPE DOUBLE PRECISION[];
