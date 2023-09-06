import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
	const faces = await prisma.face.findMany({ include: { person: true } });
	console.log(faces);
}

main()
	.then(async () => {
		await prisma.$disconnect();
	})
	.catch(async (e) => {
		console.error(e);
		await prisma.$disconnect();
		process.exit(1);
	});
