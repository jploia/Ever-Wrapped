import Image from "next/image";

export default function Home() {
  return (
    <div className="bg-burgundy grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:center">
        <h1>EverWrapped</h1>
        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <h2>Top Songs</h2>
          <h2>Top Artists</h2>
          <h2>Top Genres</h2>
          <h2>Top App</h2>
          <h2>Minutes Listened</h2>
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center"></footer>
    </div>
  );
}
