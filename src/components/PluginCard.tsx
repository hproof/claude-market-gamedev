import Link from "next/link";
import { Plugin, formatDownloads, formatPrice } from "@/lib/plugins";

interface PluginCardProps {
  plugin: Plugin;
  featured?: boolean;
}

export default function PluginCard({ plugin, featured = false }: PluginCardProps) {
  return (
    <Link
      href={`/plugins/${plugin.id}`}
      className={`block bg-gray-800 border rounded-xl overflow-hidden hover:border-purple-500 hover:shadow-lg hover:shadow-purple-900/20 transition-all group ${
        featured ? "border-purple-500/50" : "border-gray-700"
      }`}
    >
      <div className="p-5">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 bg-gray-700 rounded-xl flex items-center justify-center text-2xl flex-shrink-0 group-hover:bg-gray-600 transition-colors">
            {plugin.icon}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-white font-semibold text-base group-hover:text-purple-300 transition-colors truncate">
                {plugin.name}
              </h3>
              {featured && (
                <span className="text-xs bg-purple-600/30 text-purple-300 border border-purple-500/40 px-2 py-0.5 rounded-full flex-shrink-0">
                  精选
                </span>
              )}
            </div>
            <p className="text-gray-400 text-xs mt-0.5">by {plugin.author}</p>
          </div>
        </div>

        <p className="text-gray-300 text-sm mt-3 line-clamp-2 leading-relaxed">
          {plugin.description}
        </p>

        <div className="flex flex-wrap gap-1.5 mt-3">
          {plugin.tags.slice(0, 3).map((tag) => (
            <span
              key={tag}
              className="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded-md"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className="px-5 py-3 bg-gray-900/50 border-t border-gray-700 flex items-center justify-between">
        <div className="flex items-center gap-4 text-xs text-gray-400">
          <span className="flex items-center gap-1">
            <span className="text-yellow-400">★</span>
            <span className="text-white font-medium">{plugin.rating}</span>
            <span>({plugin.reviewCount})</span>
          </span>
          <span>{formatDownloads(plugin.downloads)} 下载</span>
        </div>
        <span
          className={`text-sm font-semibold ${
            plugin.price === "free" ? "text-green-400" : "text-blue-400"
          }`}
        >
          {formatPrice(plugin.price)}
        </span>
      </div>
    </Link>
  );
}
