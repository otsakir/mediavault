import type { Metadata } from "next";
import "./globals.css";

// export const metadata: Metadata = {
//   title: "Mediavault",
//   description: "React/Next UI",
// };

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="text-slate-700">
         {children}
      </body>
    </html>
  );
}

