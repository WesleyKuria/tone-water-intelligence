import type { Metadata } from "next";
import { Inter, Crimson_Text, DM_Sans } from "next/font/google";
import "maplibre-gl/dist/maplibre-gl.css";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter-sans",
  subsets: ["latin"],
});

const crimsonText = Crimson_Text({
  variable: "--font-crimson",
  weight: ["400", "600"],
  subsets: ["latin"],
  style: ["normal", "italic"],
});

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Tone — Commercial Water Intelligence & Reuse Engine",
  description: "Droplet-level commercial rainwater harvesting & water reuse prospecting platform.",
  authors: [{ name: "Wesley Kuria" }],
  creator: "Wesley Kuria",
  publisher: "Tone Intelligence",
  keywords: [
    "Tone",
    "Water Intelligence",
    "Rainwater Harvesting",
    "Commercial Real Estate",
    "Water Reuse",
    "Sustainability",
    "ESG",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${crimsonText.variable} ${dmSans.variable} h-full antialiased`}
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col bg-[#080d1a]" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
