import type { Metadata } from "next";
import "./globals.css";
import {AuthProvider} from "@/app/context/AuthContext";
import {getUserInfo} from "@/app/lib/auth";
import {UserInfo} from "@/app/lib/types";

// export const metadata: Metadata = {
//   title: "Mediavault",
//   description: "React/Next UI",
// };

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

    const userinfo = await getUserInfo()

    console.log('userinfo: ', userinfo)

    return (
    <html lang="en">
      <body className="text-slate-700">
        <AuthProvider>
            user: {userinfo.username}
            {children}
        </AuthProvider>
      </body>
    </html>
    );
}

