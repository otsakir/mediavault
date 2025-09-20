'use client'

import {usePathname} from "next/navigation";
import Link from "next/link";
import {Trash} from "lucide-react";
import {deleteBucket} from "@/app/lib/actions";
import {useState} from "react";
import {useActionState} from "react";


export function MainMenu({menuitems}) {
    const pathname = usePathname()

        return <div className = "flex gap-4">
                {
                    menuitems.map((item) => {
                        return pathname === item.href ? <span key={item.href} className='underline'>{item.label}</span> :
                            <Link key={item.href} className='hover:underline' href={item.href}>{item.label}</Link>
                    })
                }
        </div>
}


export function TrashButton({bucket}) {

    const [pending, setPending] = useState(false);

    async function trashClicked() {
        setPending(true)
        const response =  await deleteBucket(bucket.id)
        if (response?.error) {
            setPending(false)
        }
    }

    return <button disabled={pending} onClick={trashClicked}>
            <div className='bg-teal-200 rounded-md p-2 mb-2 hover:bg-teal-400'>
                <Trash className="h-4 w-4 text-gray-600 transition-colors"/>
            </div>
    </button>

}

export function BucketForm({serverFunction, initialState, bucketId}) {

    const [formState, formAction, isPending] = useActionState(serverFunction, initialState)

    return <form action={formAction}>
        <div className="mb-4">
            <label className="block">Title</label>
            <input defaultValue={formState.title} type='text' name='title'
                   className="shadow appearance-none border rounded w-full py-2 px-3 mb-3 leading-tight focus:outline-none focus:shadow-outline"/>
        </div>
        <div className="mb-4">
            <label className="block">Description</label>
            <textarea defaultValue={formState.description} name='description'
                      className="h-40 shadow appearance-none border rounded w-full py-2 px-3 mb-3 leading-tight focus:outline-none focus:shadow-outline"/>
        </div>
        {bucketId ? <input type='hidden' name='id' value={bucketId} /> : ''}
        <input className="hover:bg-red-500 text-white px-4 p-2 bg-black rounded-md" type="submit" value={bucketId ? 'Update' : 'Create'}/>
    </form>
}