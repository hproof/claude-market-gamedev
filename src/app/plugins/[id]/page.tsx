import { notFound } from "next/navigation";
import Link from "next/link";
import { getPluginById, CATEGORIES, formatDownloads, formatPrice } from "@/lib/plugins";

interface PluginDetailPageProps {
  params: Promise<{ id: string }>;
}

export default async function PluginDetailPage({ params }: PluginDetailPageProps) {
  const { id } = await params;
  const plugin = getPluginById(id);

  if (!plugin) {
    notFound();
  }

  const category = CATEGORIES.find((c) => c.id === plugin.category);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500 mb-8 flex items-center gap-2">
        <Link href="/" className="hover:text-gray-300 transition-colors">首页</Link>
        <span>/</span>
        <Link href="/plugins" className="hover:text-gray-300 transition-colors">插件</Link>
        <span>/</span>
        {category && (
          <>
            <Link href={"/plugins?category=" + category.id} className="hover:text-gray-300 transition-colors">
              {category.label}
            </Link>
            <span>/</span>
          </>
        )}
        <span className="text-gray-300">{plugin.name}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-8">
          {/* Plugin Header */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6">
            <div className="flex items-start gap-5">
              <div className="w-16 h-16 bg-gray-700 rounded-xl flex items-center justify-center text-3xl flex-shrink-0">
                {plugin.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 flex-wrap">
                  <h1 className="text-2xl font-bold text-white">{plugin.name}</h1>
                  {plugin.featured && (
                    <span className="text-xs bg-purple-600/30 text-purple-300 border border-purple-500/40 px-2 py-1 rounded-full">
                      精选
                    </span>
                  )}
                </div>
                <p className="text-gray-400 text-sm mt-1">by {plugin.author} · v{plugin.version}</p>
                <p className="text-gray-300 mt-3 leading-relaxed">{plugin.description}</p>
                <div className="flex flex-wrap gap-2 mt-3">
                  {plugin.tags.map((tag) => (
                    <span key={tag} className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded-md">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Description */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">插件介绍</h2>
            <div className="text-gray-300 text-sm leading-relaxed whitespace-pre-line">
              {plugin.longDescription}
            </div>
          </div>

          {/* Features */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">主要功能</h2>
            <ul className="space-y-3">
              {plugin.features.map((feature) => (
                <li key={feature} className="flex items-start gap-3 text-sm text-gray-300">
                  <span className="text-purple-400 mt-0.5 flex-shrink-0">✓</span>
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Requirements */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">系统要求</h2>
            <ul className="space-y-2">
              {plugin.requirements.map((req) => (
                <li key={req} className="flex items-start gap-3 text-sm text-gray-300">
                  <span className="text-blue-400 mt-0.5 flex-shrink-0">→</span>
                  <span>{req}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Changelog */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white mb-4">版本历史</h2>
            <div className="space-y-4">
              {plugin.changelog.map((entry) => (
                <div key={entry.version} className="flex gap-4">
                  <div className="flex-shrink-0 w-16 text-right">
                    <span className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded font-mono">
                      v{entry.version}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-300">{entry.notes}</p>
                    <p className="text-xs text-gray-500 mt-1">{entry.date}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-5">
          {/* Install Card */}
          <div className="bg-gray-800 border border-gray-700 rounded-2xl p-6 sticky top-24">
            <div className="text-3xl font-bold mb-1">
              {plugin.price === "free" ? (
                <span className="text-green-400">免费</span>
              ) : (
                <span className="text-white">{formatPrice(plugin.price)}</span>
              )}
            </div>
            {plugin.price !== "free" && (
              <p className="text-gray-500 text-xs mb-4">一次性付款，终身更新</p>
            )}
            <button className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 rounded-xl transition-colors mt-4">
              {plugin.price === "free" ? "免费下载" : "立即购买"}
            </button>
            <button className="w-full bg-gray-700 hover:bg-gray-600 text-white font-medium py-2.5 rounded-xl transition-colors mt-3 text-sm">
              查看文档
            </button>

            <hr className="border-gray-700 my-5" />

            <dl className="space-y-3 text-sm">
              <div className="flex justify-between">
                <dt className="text-gray-400">当前版本</dt>
                <dd className="text-white font-mono">v{plugin.version}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-400">最后更新</dt>
                <dd className="text-white">{plugin.updatedAt}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-400">下载量</dt>
                <dd className="text-white">{formatDownloads(plugin.downloads)}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-400">评分</dt>
                <dd className="text-white flex items-center gap-1">
                  <span className="text-yellow-400">★</span>
                  {plugin.rating}
                  <span className="text-gray-500">({plugin.reviewCount})</span>
                </dd>
              </div>
              {category && (
                <div className="flex justify-between">
                  <dt className="text-gray-400">类别</dt>
                  <dd>
                    <Link
                      href={"/plugins?category=" + category.id}
                      className="text-purple-400 hover:text-purple-300 transition-colors"
                    >
                      {category.label}
                    </Link>
                  </dd>
                </div>
              )}
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}
