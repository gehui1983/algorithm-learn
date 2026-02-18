uv add 和 uv pip install 都是高速度的包安装工具，主要区别在于项目依赖管理逻辑：uv add 是现代项目依赖管理工具，会自动将包添加到 pyproject.toml 文件并锁依赖；而 uv pip install 类似于 pip 命令，仅在当前环境中安装包，不管理配置文件。 
核心区别对比
uv add <package>：
适用场景：项目开发、管理 pyproject.toml。
行为：自动将包添加到 pyproject.toml 的 dependencies 字段。
锁定：更新 uv.lock 文件，保证环境一致性。
范式：声明式（你想要什么包，自动安装并记录）。
uv pip install <package>：
适用场景：临时安装、脚本依赖、兼容传统 pip 习惯。
行为：安装包到当前虚拟环境（或系统环境）。
锁定：不修改 pyproject.toml，不生成 lock 文件。
范式：命令式（你让它安装，它就安装）。 
简单总结
如果你在做 Python 项目开发，推荐使用 uv add，它能帮助你管理和同步依赖；如果是临时下载某个库测试或处理一次性脚本，使用 uv pip install



uv init
初始化一個新專案，建立 pyproject.toml 檔案與推薦的專案結構 (包含 .git 與 .gitignore)。

uv init my_app
uv add
新增一個或多個套件至專案。如果 .venv 不存在，將會自動建立。同時更新 pyproject.toml 與 uv.lock。

uv add flask pydantic
➖ uv remove
從專案中移除套件，並自動更新依賴檔案。
uv remove flask

uv sync
根據 uv.lock 檔案快速同步虛擬環境，確保環境 100% 可重現。即使 .venv 被刪除也能立即重建。
uv sync

uv run
在 uv 管理的虛擬環境中執行 Python 腳本或任何命令，無需手動 activate 環境。
uv run python main.py

uv add --dev
新增僅供開發時使用的依賴套件 (如 ipykernel)，並將其分類至 [tool.uv.dev-dependencies] 中。
uv add ipykernel --dev


uv tool install
取代 pipx，在全域安裝 Python 命令列工具 (如 ruff)，並將其安裝至獨立的環境中。
uv tool install ruff

uvx
(uv tool run 的縮寫) 在一個暫時環境中執行工具，使用後即丟棄，不汙染系統。
uvx ruff check .

uv tree
以樹狀結構視覺化顯示專案的依賴關係，幫助理解套件之間的關聯。
uv tree

uv run --python <version>
在執行命令時動態指定 Python 版本。uv 會自動尋找或下載該版本，並在隔離環境中執行。
使用 Python 3.10 執行腳本
uv run --python 3.10 main.py
使用 3.12 版本的 CPython 啟動 REPL
uv run --python cpython@3.12 python
執行任意命令
uv run --python 3.11 -- python -c "import sys; print(sys.version)"

支援的版本格式：

精確版本: 3.12.3
次要版本: 3.12 (自動選擇最新修正版本)
主要版本: 3 (自動選擇最新版)
版本範圍: ">=3.12,<3.13"

uv python pin
為目前專案鎖定一個預設 Python 版本。此命令會建立一個 .python-version 檔案。

uv python pin 3.12
之後執行的 uv run 或 uv init 將會自動使用這個版本。

uv init --python <version>
在初始化新專案時直接指定 Python 版本需求。

uv init my-new-app --python 3.12
這會自動在 pyproject.toml 中寫入 requires-python = ">=3.12" 並建立 .python-version 檔案。


關鍵特性：全自動環境
uv 的版本管理核心優勢在於自動化，讓合作成員無需擔心配置：

自動下載：若系統未安裝 --python 指定的版本，uv 會自動從 GitHub 下載並快取該版本。
無縫合作：團隊成員只需執行 uv run 或 uv sync，uv 會自動處理所有 Python 版本和環境依賴問題。
環境隔離：每次執行都會在乾淨的虛擬環境中進行，確保依賴不互相干擾。



pip install -e .

0.uv init  --创建工程
1.采用 python -m venv .venv ---生成虚拟环境
2.uv add 安装包