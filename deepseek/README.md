# DeepSeek辅助工作

独立本体位于`F:\DeepSeekHarness`，本项目只保存工作规范和启动入口。运行时、加密凭据、会话、缓存、资料副本和结果全部保存在F盘独立目录。

**论文、术语说明、README、译文与短段落由主助手直接写改。** DeepSeek只承担大批量、低风险、耗时的资料通读、检索、逐项对照和取证，给主助手内部报告。报告只看事实与定位，不为措辞润色；不满意就简短反馈，让它补查或改报告。

每次提供资料副本，在独立Jobs目录运行。研究配置关闭文件write／edit、Shell、子代理、后台任务和工作流。主管审核报告，亲自决定如何改文档。

```powershell
./deepseek/Invoke-Review.ps1 -TaskFile ./deepseek/tasks/full_text_review.md -InputFiles ./某篇完整原文.txt
./deepseek/Follow-Up.ps1 -JobDirectory F:\DeepSeekHarness\Jobs\某任务 -Feedback '把第3项引用前后两段补全，并查一下相反证据。'
```

默认medium；机械任务可选low，需要推理的原典问题才用high。终止原因不是completed就不收作成功，不盲目重复整项任务。PDF先完整提取为保留原页码的文本，缺页与无法提取部分列明。

通读要求见[规范](tasks/full_text_review.md)：按顺序读完，核对实际返回的页／行范围与截断情况，报告原话、上下文、定位及未找到的内容。传入全文不等于已经读完全文，不把搜索摘要当作全文证据。
