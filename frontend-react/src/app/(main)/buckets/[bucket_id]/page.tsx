import {updateBucket, getBucket} from "@/app/lib/actions";
import Link from "next/link";
import Image from "next/image";
import {Suspense} from "react";
import {GenericSkeleton} from "@/app/ui/skeletons";
import {BucketForm} from "@/app/ui/components";

export default async function BucketPage({params}: {params: {bucket_id: bigint}}){

    const {bucket_id} = await(params)
    const bucket = await getBucket( bucket_id)



    return (<div className='text-slate-700'>
        <div className="flex items-center justify-between mb-4 border-b border-slate-200 py-2">
            <h1 className="text-3xl">Bucket {bucket.title}</h1>
        </div>

        <BucketForm serverFunction={updateBucket} initialState={bucket} bucketId={bucket_id} />

        {/*<Suspense fallback={<GenericSkeleton/>}>*/}
        {/*    <BucketsList/>*/}
        {/*</Suspense>*/}
    </div>)
}