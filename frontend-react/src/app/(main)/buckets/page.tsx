import {GenericSkeleton} from "@/app/ui/skeletons";
import {Suspense} from "react";
import Image from "next/image";
import Link from 'next/link'


async function BucketsList() {
    // TODO - error handling
    const response = await fetch('http://localhost:8000/api/buckets')
    const data = await response.json()

    return <ul>
        {data.map((bucket) => {
            return <li key={bucket.id}>{bucket.title}</li>
        })}
    </ul>

}

export default async function Buckets() {

    return (<div className="text-slate-700">

        <div className="flex items-center justify-between mb-4 border-b border-slate-200 py-2">
            <h1 className="text-3xl">Buckets</h1>
            {/*{% if perms.buckets.add_bucket %}*/}
            <Link href='/buckets/new'>
                <div className='p-2 hover:text-blue-800 hover:bg-blue-100 rounded-md'>
                    <Image src="/icons/folder-plus.svg" width={24} height={24} alt={'add new bucket'}/>
                </div>
            </Link>
            {/*{%  endif %}*/}
        </div>

        <Suspense fallback={<GenericSkeleton/>}>
            <BucketsList/>
        </Suspense>

    </div>)
}