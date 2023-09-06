import os
import face_recognition
import hashlib
import asyncio

from prisma_client.client import Prisma


async def run():
    db = Prisma()
    await db.connect()
    print('connected to db')

    root_folder = "./test_folder"
    hash_to_file_paths = {}
    hash_to_face_encodings = {}

    def get_image(dir_path, file):
        file_path = os.path.abspath(os.path.join(dir_path, file))
        image = face_recognition.load_image_file(file_path)
        return file_path, image

    def hash_and_store_file(file_path, image):
        md5 = hashlib.md5(image).hexdigest()
        if md5 in hash_to_file_paths:
            hash_to_file_paths[md5] += [file_path]
            return
        hash_to_file_paths[md5] = [file_path]
        return md5

    for dirpath, dirs, files in os.walk(root_folder):
        for file in files:
            print('processing', file)
            file_path, image = get_image(dirpath, file)
            md5 = hash_and_store_file(file_path, image)
            face_locations = face_recognition.face_locations(image, model="cnn")
            face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)
            hash_to_face_encodings[md5] = [face_encoding.tolist() for face_encoding in face_encodings]

    print('storing results in db')
    for hash in hash_to_file_paths.keys():
        image = await db.image.find_first(where={"md5" : hash})
        if image is None:
            image = await db.image.create(
                {
                    "md5": hash,
                    "paths": hash_to_file_paths[hash],

                }
            )
            print('created image', image)
        else:
            image = await db.image.update(where={"id": image.id}, data={"paths": {"set": hash_to_file_paths[hash]}})
            print('updated image', image)
        
        face_encodings = hash_to_face_encodings[hash]

        for face_encoding in face_encodings:
            proposed_person = await db.person.create(data={'name': 'unknown'})
            print('created person', proposed_person)
            face = await db.face.create(
                data={
                    'image': {'connect': {'id': image.id}}, 
                    'person': {'connect': {'id': proposed_person.id}},
                    'embedding': face_encoding,
                }
            )
            
            print('created person and face', proposed_person, face)

    await db.disconnect()

if __name__ == '__main__':
    asyncio.run(run())