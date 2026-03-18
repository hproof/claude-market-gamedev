import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center text-white text-sm font-bold">
              C
            </div>
            <span className="text-white font-bold text-lg tracking-tight">
              Claude <span className="text-purple-400">GameDev</span> Market
            </span>
          </Link>

          <div className="flex items-center gap-6">
            <Link
              href="/plugins"
              className="text-gray-300 hover:text-white text-sm font-medium transition-colors"
            >
              浏览插件
            </Link>
            <a
              href="https://docs.anthropic.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-300 hover:text-white text-sm font-medium transition-colors"
            >
              文档
            </a>
            <Link
              href="/plugins"
              className="bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
            >
              发布插件
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
