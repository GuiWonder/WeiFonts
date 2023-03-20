namespace toWinFonts
{
    partial class FormMain
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.buttonStart = new System.Windows.Forms.Button();
            this.labeli1 = new System.Windows.Forms.Label();
            this.labelo = new System.Windows.Forms.Label();
            this.textBoxIn = new System.Windows.Forms.TextBox();
            this.textBoxOut = new System.Windows.Forms.TextBox();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.panelMain = new System.Windows.Forms.Panel();
            this.comboBox2 = new System.Windows.Forms.ComboBox();
            this.comboBox1 = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.linkLabelOut = new System.Windows.Forms.LinkLabel();
            this.linkLabelIn = new System.Windows.Forms.LinkLabel();
            this.linkLabel1 = new System.Windows.Forms.LinkLabel();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.checkBoxRmTTF = new System.Windows.Forms.CheckBox();
            this.panelMain.SuspendLayout();
            this.SuspendLayout();
            // 
            // buttonStart
            // 
            this.buttonStart.Location = new System.Drawing.Point(387, 12);
            this.buttonStart.Name = "buttonStart";
            this.buttonStart.Size = new System.Drawing.Size(75, 23);
            this.buttonStart.TabIndex = 6;
            this.buttonStart.Text = "开始";
            this.buttonStart.UseVisualStyleBackColor = true;
            this.buttonStart.Click += new System.EventHandler(this.ButtonStart_Click);
            // 
            // labeli1
            // 
            this.labeli1.AutoSize = true;
            this.labeli1.Location = new System.Drawing.Point(3, 87);
            this.labeli1.Name = "labeli1";
            this.labeli1.Size = new System.Drawing.Size(65, 12);
            this.labeli1.TabIndex = 1;
            this.labeli1.Text = "* 输入字体";
            // 
            // labelo
            // 
            this.labelo.AutoSize = true;
            this.labelo.Location = new System.Drawing.Point(3, 123);
            this.labelo.Name = "labelo";
            this.labelo.Size = new System.Drawing.Size(65, 12);
            this.labelo.TabIndex = 2;
            this.labelo.Text = "* 保存目录";
            // 
            // textBoxIn
            // 
            this.textBoxIn.AllowDrop = true;
            this.textBoxIn.Location = new System.Drawing.Point(74, 84);
            this.textBoxIn.Name = "textBoxIn";
            this.textBoxIn.Size = new System.Drawing.Size(353, 21);
            this.textBoxIn.TabIndex = 2;
            this.textBoxIn.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.textBoxIn.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // textBoxOut
            // 
            this.textBoxOut.AllowDrop = true;
            this.textBoxOut.Location = new System.Drawing.Point(74, 120);
            this.textBoxOut.Name = "textBoxOut";
            this.textBoxOut.Size = new System.Drawing.Size(353, 21);
            this.textBoxOut.TabIndex = 4;
            this.textBoxOut.DragDrop += new System.Windows.Forms.DragEventHandler(this.TextBox_DragDrop);
            this.textBoxOut.DragEnter += new System.Windows.Forms.DragEventHandler(this.TextBox_DragEnter);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.Filter = "字體文件|*.ttf;*.otf|所有文件|*.*";
            // 
            // panelMain
            // 
            this.panelMain.Controls.Add(this.checkBoxRmTTF);
            this.panelMain.Controls.Add(this.comboBox2);
            this.panelMain.Controls.Add(this.comboBox1);
            this.panelMain.Controls.Add(this.label2);
            this.panelMain.Controls.Add(this.label1);
            this.panelMain.Controls.Add(this.labeli1);
            this.panelMain.Controls.Add(this.labelo);
            this.panelMain.Controls.Add(this.linkLabelOut);
            this.panelMain.Controls.Add(this.textBoxIn);
            this.panelMain.Controls.Add(this.linkLabelIn);
            this.panelMain.Controls.Add(this.textBoxOut);
            this.panelMain.Controls.Add(this.buttonStart);
            this.panelMain.Location = new System.Drawing.Point(13, 13);
            this.panelMain.Name = "panelMain";
            this.panelMain.Size = new System.Drawing.Size(478, 181);
            this.panelMain.TabIndex = 18;
            // 
            // comboBox2
            // 
            this.comboBox2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox2.FormattingEnabled = true;
            this.comboBox2.Items.AddRange(new object[] {
            "自动",
            "Thin",
            "ExtraLight",
            "Light",
            "Semilight",
            "DemiLight",
            "Normal",
            "Regular",
            "Medium",
            "Demibold",
            "SemiBold",
            "Bold",
            "Black",
            "Heavy"});
            this.comboBox2.Location = new System.Drawing.Point(74, 49);
            this.comboBox2.Name = "comboBox2";
            this.comboBox2.Size = new System.Drawing.Size(286, 20);
            this.comboBox2.TabIndex = 1;
            // 
            // comboBox1
            // 
            this.comboBox1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox1.FormattingEnabled = true;
            this.comboBox1.Items.AddRange(new object[] {
            "微软雅黑、微软雅黑 UI",
            "微軟正黑體、微軟正黑體 UI",
            "細明體、新細明體、細明體_HKSCS",
            "宋体、新宋体",
            "黑体",
            "MS Gothic、MS UI Gothic、MS PGothic",
            "MS Mincho、MS PMincho",
            "Meiryo、Meiryo UI",
            "Malgun Gothic",
            "Yu Gothic、Yu Gothic UI",
            "Yu Mincho",
            "Batang、BatangChe、Gungsuh、GungsuhChe",
            "Gulim、GulimChe、Dotum、DotumChe",
            "以上所有无衬线字体",
            "以上所有衬线字体",
            "以上所有字体",
            "細明體-ExtB、新細明體-ExtB、細明體_HKSCS-ExtB",
            "宋体-ExtB"});
            this.comboBox1.Location = new System.Drawing.Point(74, 14);
            this.comboBox1.Name = "comboBox1";
            this.comboBox1.Size = new System.Drawing.Size(286, 20);
            this.comboBox1.TabIndex = 0;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(39, 52);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(29, 12);
            this.label2.TabIndex = 20;
            this.label2.Text = "字重";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(15, 17);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(53, 12);
            this.label1.TabIndex = 20;
            this.label1.Text = "目标字体";
            // 
            // linkLabelOut
            // 
            this.linkLabelOut.AutoSize = true;
            this.linkLabelOut.Location = new System.Drawing.Point(433, 124);
            this.linkLabelOut.Name = "linkLabelOut";
            this.linkLabelOut.Size = new System.Drawing.Size(29, 12);
            this.linkLabelOut.TabIndex = 5;
            this.linkLabelOut.TabStop = true;
            this.linkLabelOut.Text = "选择";
            this.linkLabelOut.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabelOut_LinkClicked);
            // 
            // linkLabelIn
            // 
            this.linkLabelIn.AutoSize = true;
            this.linkLabelIn.Location = new System.Drawing.Point(433, 88);
            this.linkLabelIn.Name = "linkLabelIn";
            this.linkLabelIn.Size = new System.Drawing.Size(29, 12);
            this.linkLabelIn.TabIndex = 3;
            this.linkLabelIn.TabStop = true;
            this.linkLabelIn.Text = "选择";
            this.linkLabelIn.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabelIn_LinkClicked);
            // 
            // linkLabel1
            // 
            this.linkLabel1.AutoSize = true;
            this.linkLabel1.Location = new System.Drawing.Point(28, 208);
            this.linkLabel1.Name = "linkLabel1";
            this.linkLabel1.Size = new System.Drawing.Size(53, 12);
            this.linkLabel1.TabIndex = 21;
            this.linkLabel1.TabStop = true;
            this.linkLabel1.Text = "项目主页";
            this.linkLabel1.LinkClicked += new System.Windows.Forms.LinkLabelLinkClickedEventHandler(this.LinkLabel1_LinkClicked);
            // 
            // checkBoxRmTTF
            // 
            this.checkBoxRmTTF.AutoSize = true;
            this.checkBoxRmTTF.Checked = true;
            this.checkBoxRmTTF.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxRmTTF.Location = new System.Drawing.Point(17, 157);
            this.checkBoxRmTTF.Name = "checkBoxRmTTF";
            this.checkBoxRmTTF.Size = new System.Drawing.Size(156, 16);
            this.checkBoxRmTTF.TabIndex = 21;
            this.checkBoxRmTTF.Text = "TTC 打包完成后移除 TTF";
            this.checkBoxRmTTF.UseVisualStyleBackColor = true;
            // 
            // FormMain
            // 
            this.AcceptButton = this.buttonStart;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Window;
            this.ClientSize = new System.Drawing.Size(506, 229);
            this.Controls.Add(this.linkLabel1);
            this.Controls.Add(this.panelMain);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "FormMain";
            this.ShowIcon = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = " 创建 Windows 代替字体";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.FormMain_FormClosing);
            this.Load += new System.EventHandler(this.FormMain_Load);
            this.panelMain.ResumeLayout(false);
            this.panelMain.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Label labeli1;
        private System.Windows.Forms.Label labelo;
        private System.Windows.Forms.TextBox textBoxIn;
        private System.Windows.Forms.TextBox textBoxOut;
        private System.Windows.Forms.Button buttonStart;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.Panel panelMain;
        private System.Windows.Forms.LinkLabel linkLabelOut;
        private System.Windows.Forms.LinkLabel linkLabelIn;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox comboBox2;
        private System.Windows.Forms.ComboBox comboBox1;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.LinkLabel linkLabel1;
        private System.Windows.Forms.CheckBox checkBoxRmTTF;
    }
}

