import Link from "next/link";
import { getFeaturedPlugins, CATEGORIES } from "@/lib/plugins";
import PluginCard from "@/components/PluginCard";

export default function Home() {
  const featured = getFeaturedPlugins();

  return (
    <div>
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-purple-950/30 to-gray-900 py-24 px-4">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent pointer-events-none" />
        <div className="max-w-4xl mx-auto text-center relative">
          <div className="inline-flex items-center gap-2 bg-purple-900/40 border border-purple-700/50 text-purple-300 text-sm px-4 py-1.5 rounded-full mb-6">
            <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" />
            由 Claude AI 驱动的游戏开发工具生态
          </div>
          <h1 className="text-5xl font-bold text-white leading-tight mb-6">
            游戏开发者的
            <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              {" "}Claude{" "}
            </span>
            插件市场
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed mb-10">
            发现、安装并集成专为游戏开发设计的 Claude AI 插件。
            从 NPC 对话到程序化生成，AI 助力每个开发环节。
          </p>
          <div className="flex items-center justify-center gap-4 flex-wrap">
            <Link
              href="/plugins"
              className="bg-purple-600 hover:bg-purple-700 text-white font-semibold px-8 py-3 rounded-xl transition-colors text-lg"
            >
              浏览所有插件
            </Link>
            <Link
              href="/plugins?category=game-engine"
              className="bg-gray-800 hover:bg-gray-700 border border-gray-700 text-white font-semibold px-8 py-3 rounded-xl transition-colors text-lg"
            >
              引擎集成插件
            </Link>
          </div>

          <div className="mt-16 grid grid-cols-3 gap-6 max-w-lg mx-auto">
            {[
              { value: "12+", label: "款插件" },
              { value: "233K+", label: "总下载量" },
              { value: "10", label: "开发类别" },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-2xl font-bold text-white">{stat.value}</div>
                <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-2xl font-bold text-white mb-2">按类别浏览</h2>
        <p className="text-gray-400 mb-8">探索覆盖游戏开发全流程的 AI 插件</p>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {CATEGORIES.map((cat) => (
            <Link
              key={cat.id}
              href={"/plugins?category=" + cat.id}
              className="bg-gray-800 border border-gray-700 hover:border-purple-500 rounded-xl p-4 text-center group transition-all"
            >
              <div className="text-3xl mb-2">{cat.icon}</div>
              <div className="text-white text-sm font-medium group-hover:text-purple-300 transition-colors">
                {cat.label}
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Plugins */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-white mb-1">精选插件</h2>
            <p className="text-gray-400 text-sm">社区推荐的高质量 Claude 游戏开发插件</p>
          </div>
          <Link href="/plugins" className="text-purple-400 hover:text-purple-300 text-sm font-medium transition-colors">
            查看全部 →
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {featured.map((plugin) => (
            <PluginCard key={plugin.id} plugin={plugin} featured />
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        <div className="bg-gradient-to-r from-purple-900/50 to-blue-900/50 border border-purple-700/40 rounded-2xl p-10 text-center">
          <h2 className="text-2xl font-bold text-white mb-3">想发布自己的插件？</h2>
          <p className="text-gray-400 mb-6 max-w-xl mx-auto">
            将您的 Claude 游戏开发工具分享给全球开发者，加入我们不断壮大的插件生态。
          </p>
          <Link
            href="/plugins"
            className="bg-white text-gray-900 font-semibold px-8 py-3 rounded-xl hover:bg-gray-100 transition-colors inline-block"
          >
            立即发布插件
          </Link>
        </div>
      </section>
    </div>
  );
}
