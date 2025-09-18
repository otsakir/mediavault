

export default function NewBucket() {

    async function createBucket(formData: FormData) {
        'use server';

        const rawFormData = {
            title: formData.get('title'),
            description: formData.get('description'),
        };
        // Test it out:
        console.log("rawFormData:", rawFormData);
    }

    return (
        <div className="text-slate-700">
            <div className="flex items-center justify-between mb-4 border-b py-2 border-slate-200">
                <h1 className="text-3xl">New bucket</h1>
            </div>
            <form action={createBucket}>
                <div className="mb-4">
                    <label className="block">Title</label>
                    <input type='text' name='title' className="shadow appearance-none border border-slate-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"/>
                </div>
                <div className="mb-4">
                    <label className="block">Description</label>
                    <textarea name='description' className="h-40 shadow appearance-none border border-slate-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"/>
                </div>
                <input className="hover:bg-red-500 text-white px-4 p-2 bg-black rounded-md" type="submit" value="Save"/>
            </form>
        </div>
    )

}