# KangRollGeneCancer
KangRollGeneCancer for  pypi
-ini
-for link :

--

----
这样的目录结构， Work：
KangRollGeneCancer/
├── KangRollGeneCancer/   # 包目录
│   ├── __init__.py
│   └── analyze_gene.py
├── tests/                # 测试目录
│   └── test_kangrollgenecancer.py
├── KangRollGeneCancer.egg-info/
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── build/
├── dist/
├── README.md
├── setup.py
└── version.txt


-
----成功， 

制作自动编译Bash脚本 

要将您描述的发布流程自动化成一个脚本，您可以使用 Bash 脚本来完成。下面是一个简单的脚本示例，该脚本将执行您所描述的步骤：

自动更新 setup.py 中的版本号。
清理旧的构建文件。
构建新的发行版并上传到 PyPI。
卸载旧版本并安装新版本。

---
我建议用这样的方法似乎更好一点，我们不要在bash中更新setup.py.  我们可否制作一个 更新setup.py  的py程序，而后通过.sh 调用这个更新setup.py 的程序来更新序号。 而后调用更新后的setup.py. 这样逻辑就顺了。而且可以减小bash内的复杂性，以及bash 的负担。可否？
-


为了在您的工作目录 `research_project_cancer_genomics` 和装载 PyPI 库源码的文件夹之间创建相互链接，您可以使用软链接（symbolic links）。这将允许您在两个文件夹之间快速切换，同时保持它们的独立性和组织结构。

假设您的 PyPI 库源码文件夹名为 `KangRollGeneCancer`（位于某个路径下），您可以按照以下步骤操作：

### 从 `research_project_cancer_genomics` 链接到 `KangRollGeneCancer`

1. 打开终端。

2. 切换到 `research_project_cancer_genomics` 目录：

   ```bash
   cd /path/to/research_project_cancer_genomics
   ```

3. 创建一个指向 `KangRollGeneCancer` 的软链接：

   ```bash
   ln -s /path/to/KangRollGeneCancer KangRollGeneCancer
   ```

现在，在 `research_project_cancer_genomics` 目录中，您将看到一个名为 `KangRollGeneCancer` 的链接，它指向您的 PyPI 库源码文件夹。

### 从 `KangRollGeneCancer` 链接回 `research_project_cancer_genomics`

1. 切换到 `KangRollGeneCancer` 目录：

   ```bash
   cd /path/to/KangRollGeneCancer
   ```

2. 创建一个指回 `research_project_cancer_genomics` 的软链接：

   ```bash
   ln -s /path/to/research_project_cancer_genomics research_project_cancer_genomics
   ```

现在，在 `KangRollGeneCancer` 目录中，您将看到一个名为 `research_project_cancer_genomics` 的链接，它指回您的工作目录。

### 使用这些链接

- 通过简单地输入 `cd KangRollGeneCancer` 或 `cd research_project_cancer_genomics`，您可以在这两个目录之间快速跳转。
- 这些链接像普通目录一样使用，但它们实际上是指向另一个位置的引用。

### 注意事项

- 确保软链接的源路径和目标路径是正确的。
- 如果您在一个版本控制系统（如Git）下管理这些文件夹，请注意软链接可能会对版本控制产生影响。
- 软链接在大多数情况下是透明的，但在进行某些文件操作时，需要意识到您是在操作链接本身还是链接指向的实际文件。



