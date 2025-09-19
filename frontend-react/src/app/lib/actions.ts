'use server'

import {redirect} from "next/navigation";
import {revalidatePath} from "next/cache";

export async function createBucket(prevState: any, formData: FormData) {
    'use server';

    console.log('formData:', formData)
    console.log('prevState:', prevState)

    const rawFormData = {
        title: formData.get('title'),
        description: formData.get('description'),
    };
    // Test it out:
    console.log("rawFormData:", rawFormData);

    const response = await fetch('http://localhost:8000/api/buckets', {
        method: 'POST',
        body: JSON.stringify(rawFormData),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (!response.ok) {
        return {
            error:'error creating bucket',
            title: rawFormData.title,
            description: rawFormData.description
        }
    } else {
        revalidatePath('/buckets')
        redirect('/buckets')
    }
}


export async function deleteBucket(bucket_id){
    console.log('in deleteBucket(): bucket_id:', bucket_id)

    const response = await fetch(`http://localhost:8000/api/buckets/${bucket_id}`, {
        method: 'DELETE'
    })

    // await new Promise((resolve) => setTimeout(resolve, 3000))
    if (!response.ok) {
        return {error: `can't delete bucket ${bucket_id}`}
    } else {
        revalidatePath('/buckets')
    }
}
