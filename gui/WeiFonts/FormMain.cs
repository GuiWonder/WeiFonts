using System;
using System.Text;
using System.Windows.Forms;

namespace WeiFonts
{
    public partial class FormMain : Form
    {
        readonly OpenFileDialog openFileDialog = new OpenFileDialog();
        readonly SaveFileDialog saveFileDialog = new SaveFileDialog();
        readonly FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
        readonly LinkLabel[] linkLabels;
        readonly TextBox[] textBoxes;
        readonly bool DEBUG;
        readonly string VER = "20250829";
        private string exepy;
        private readonly string path;
        private string args;
        private System.Threading.Thread thRun;

        public FormMain()
        {
            InitializeComponent();
            path = AppDomain.CurrentDomain.BaseDirectory;
            linkLabelWeb.LinkClicked += (s, e) => System.Diagnostics.Process.Start("https://github.com/GuiWonder/WeiFonts");
            comboBoxMBWin.SelectedIndex = 0;
            comboBoxWTWin.SelectedIndex = 0;
            comboBoxItWin.SelectedIndex = 0;
            linkLabels = new LinkLabel[] { linkLabelM, linkLabelInWei, linkLabelOutWei, linkLabelInWin, linkLabelOutWin, linkLabelIn1, linkLabelIn2, linkLabelIn3, linkLabelIn4, linkLabelIn5, linkLabelIn6, linkLabelOutPf };
            textBoxes = new TextBox[] { textBoxM, textBoxInWei, textBoxOutWei, textBoxInWin, textBoxOutWin, textBox1, textBox2, textBox3, textBox4, textBox5, textBox6, textBoxOutPf };

            foreach (TextBox item in textBoxes)
            {
                item.DragDrop += TextBox_DragDrop;
                item.DragEnter += TextBox_DragEnter;
            }
            foreach (LinkLabel item in linkLabels)
            {
                item.LinkClicked += LinkLabe_LinkClicked;
            }
            buttonStartWei.Click += ButtonStartWei_Click;
            buttonStartWin.Click += ButtonStartWin_Click;
            buttonStartPf.Click += ButtonStartPf_Click;
            FormClosing += FormMain_FormClosing;
            checkBoxDeep.CheckStateChanged += (s, e) => checkBoxWeiMT.Enabled = !checkBoxDeep.Checked;
            string[] startargs = Environment.GetCommandLineArgs();
            DEBUG = startargs.Length > 1 && startargs[1].ToLower() == "debug";
            label15.Text += VER;
        }


        private void ButtonStartPf_Click(object sender, System.EventArgs e)
        {
            string fileout = textBoxOutPf.Text.Trim().Trim('"');
            string[] infls = { textBox1.Text.Trim().Trim('"'), textBox2.Text.Trim().Trim('"'), textBox3.Text.Trim().Trim('"'), textBox4.Text.Trim().Trim('"'), textBox5.Text.Trim().Trim('"'), textBox6.Text.Trim().Trim('"') };
            if (!GetEXEPY())
            {
                return;
            }
            foreach (string item in infls)
            {
                if (!System.IO.File.Exists(item))
                {
                    NoFileErr(item);
                    return;
                }
            }
            if (string.IsNullOrWhiteSpace(fileout))
            {
                SellFileInfo();
                return;
            }

            string pyfile = path + "files\\weipingfang.py";
            if (!System.IO.File.Exists(pyfile))
            {
                NoSysFileErr(pyfile);
                return;
            }
            pyfile = pyfile.Replace('\\', '/');
            args = $"-X utf8 \"{pyfile}\" -o \"{fileout}\"";
            for (int i = 0; i < infls.Length; i++)
            {
                args += $" -f{i + 1} \"{infls[i].Replace('\\', '/')}\"";
            }
            if (checkBoxPfMT.Checked)
            {
                args += " -mt";
            }
            RunArgs();
        }

        private void NoFileErr(string item) => MessageBox.Show(this, $"文件{item}无效，请重新选择。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
        private void NoSysFileErr(string item) => MessageBox.Show(this, $"缺少必要文件{item}，请重新下载。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
        private void SellFileInfo() => MessageBox.Show(this, "请选择保存文件。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
        private void NoPYErr() => MessageBox.Show(this, "未能找到 Python。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);

        private void ButtonStartWin_Click(object sender, System.EventArgs e)
        {
            string filein = textBoxInWin.Text.Trim().Trim('"');
            string dirout = textBoxOutWin.Text.Trim().Trim('"');
            if (!GetEXEPY())
            {
                return;
            }
            if (!System.IO.File.Exists(filein))
            {
                NoFileErr(filein);
                return;
            }
            if (!System.IO.Directory.Exists(dirout))
            {
                MessageBox.Show(this, $"保存目录{dirout}无效，请重新选择。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            string[] tgs = { "msyh", "msjh", "mingliu", "simsun", "simhei", "deng", "msgothic", "msmincho", "meiryo", "malgun", "yugoth", "yumin", "batang", "gulim", "allsans", "allserif", "all", "mingliub", "simsunb", "simsunextg", "kaiu", "simkai", "simfang" };
            string tg = tgs[comboBoxMBWin.SelectedIndex];
            string pyfile = path + "files\\weiwin.py";
            if (!System.IO.File.Exists(pyfile))
            {
                NoSysFileErr(pyfile);
                return;
            }
            pyfile = pyfile.Replace('\\', '/');
            filein = filein.Replace('\\', '/');
            dirout = dirout.Replace('\\', '/');
            args = $"-X utf8 \"{pyfile}\" -i \"{filein}\" -d \"{dirout}\" -tg {tg}";
            if (comboBoxWTWin.SelectedIndex != 0)
            {
                args += $" -wt {comboBoxWTWin.Text}";
            }
            if (checkBoxRmTTFWin.Checked)
            {
                args += " -r";
            }
            if (comboBoxItWin.SelectedIndex == 1)
            {
                args += " -it y";
            }
            else if (comboBoxItWin.SelectedIndex == 2)
            {
                args += " -it n";
            }
            if (checkBoxWinMT.Checked)
            {
                args += " -mt";
            }
            RunArgs();
        }

        private void ButtonStartWei_Click(object sender, System.EventArgs e)
        {
            string filem = textBoxM.Text.Trim().Trim('"');
            string filein = textBoxInWei.Text.Trim().Trim('"');
            string fileout = textBoxOutWei.Text.Trim().Trim('"');
            if (!GetEXEPY())
            {
                return;
            }
            if (!System.IO.File.Exists(filein))
            {
                NoFileErr(filein);
                return;
            }
            if (!System.IO.File.Exists(filem))
            {
                NoFileErr(filem);
                return;
            }
            if (string.IsNullOrWhiteSpace(fileout))
            {
                SellFileInfo();
                return;
            }

            string pyfile = path + "files\\weiwei.py";
            if (!System.IO.File.Exists(pyfile))
            {
                NoSysFileErr(pyfile);
                return;
            }
            pyfile = pyfile.Replace('\\', '/');
            filem = filem.Replace('\\', '/');
            filein = filein.Replace('\\', '/');
            fileout = fileout.Replace('\\', '/');
            args = $"-X utf8 \"{pyfile}\" -i \"{filein}\" -o \"{fileout}\" -m \"{filem}\"";
            if (checkBoxDeep.Checked)
            {
                args += " -deep";
            }
            else if (checkBoxWeiMT.Checked)
            {
                args += " -mt";
            }
            RunArgs();
        }

        private bool GetEXEPY()
        {
            if (System.IO.File.Exists($"{path}python/python.exe"))
            {
                exepy = $"{path}python/python.exe";
                return true;
            }
            if (IsInPATH("python.exe"))
            {
                exepy = "python";
                return true;
            }
            NoPYErr();
            return false;
        }

        private void RunArgs()
        {
            tabControl1.Enabled = false;
            Cursor = Cursors.WaitCursor;
            thRun = new System.Threading.Thread(ThRun)
            {
                IsBackground = true
            };
            thRun.Start();
        }

        private void ThRun()
        {
            string err = "";
            using (System.Diagnostics.Process p = new System.Diagnostics.Process())
            {
                //p.StartInfo.StandardOutputEncoding = Encoding.UTF8;
                p.StartInfo.StandardErrorEncoding = Encoding.UTF8;
                p.StartInfo.FileName = exepy;
                p.StartInfo.Arguments = args;
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = true;
                p.StartInfo.RedirectStandardError = true;
                p.Start();
                p.ErrorDataReceived += (s, e) =>
                {
                    if (!string.IsNullOrWhiteSpace(e.Data) && (DEBUG || e.Data.Contains("Error") || e.Data.Contains("ERROR")) && !e.Data.Contains("raise"))
                    {
                        err += e.Data + "\r\n";
                    }
                };
                p.BeginErrorReadLine();
                p.WaitForExit();
                p.Close();
            }
            Invoke(new Action(delegate
            {
                tabControl1.Enabled = true;
                Cursor = Cursors.Default;
                if (err.Contains("Error:"))
                {
                    MessageBox.Show(this, err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                else
                {
                    MessageBox.Show(this, "处理完毕！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }));
        }

        private bool IsInPATH(string command)
        {
            foreach (string s in (Environment.GetEnvironmentVariable("PATH") ?? "").Split(';'))
            {
                string evpath = s.Trim();
                if (!string.IsNullOrEmpty(evpath) && System.IO.File.Exists(System.IO.Path.Combine(evpath, command)))
                {
                    return true;
                }
            }
            return false;
        }

        #region ui
        private void FormMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (thRun != null && thRun.IsAlive)
            {
                e.Cancel = true;
            }
        }

        private void LinkLabe_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (sender == linkLabelM)
            {
                openFileDialog.Filter = "字体文件|*.ttf;*.otf;*.ttc;*.otc|所有文件|*.*";
                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    textBoxM.Text = openFileDialog.FileName;
                }
            }

            else if (sender == linkLabelOutWei)
            {
                if (textBoxM.Text.ToLower().Trim().EndsWith(".ttc"))
                {
                    saveFileDialog.Filter = "字体文件|*.ttc;*.otc;*.ttf;*.otf|所有文件|*.*";
                }
                else if (textBoxM.Text.ToLower().Trim().EndsWith(".otf"))
                {
                    saveFileDialog.Filter = "字体文件|*.otf;*.ttf;*.ttc;*.otc|所有文件|*.*";
                }
                else if (textBoxM.Text.ToLower().Trim().EndsWith(".otc"))
                {
                    saveFileDialog.Filter = "字体文件|*.otc;*.ttc;*.otf;*.ttf|所有文件|*.*";
                }
                else
                {
                    saveFileDialog.Filter = "字体文件|*.ttf;*.otf;*.ttc;*.otc|所有文件|*.*";
                }
                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    textBoxOutWei.Text = saveFileDialog.FileName;
                }
            }
            else if (sender == linkLabelOutWin)
            {
                if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
                {
                    textBoxOutWin.Text = folderBrowserDialog.SelectedPath;
                }
            }
            else if (sender == linkLabelOutPf)
            {
                saveFileDialog.Filter = "字体文件|*.ttc;*.otc|所有文件|*.*";

                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    textBoxOutPf.Text = saveFileDialog.FileName;
                }

            }
            else
            {
                openFileDialog.Filter = "字体文件|*.ttf;*.otf|所有文件|*.*";
                for (int i = 0; i < textBoxes.Length; i++)
                {
                    if (linkLabels[i] == sender)
                    {
                        if (openFileDialog.ShowDialog() == DialogResult.OK)
                        {
                            textBoxes[i].Text = openFileDialog.FileName;
                        }
                        break;
                    }
                }
            }
        }

        private void TextBox_DragDrop(object sender, DragEventArgs e) => ((TextBox)sender).Text = ((System.Array)e.Data.GetData(DataFormats.FileDrop)).GetValue(0).ToString();
        private void TextBox_DragEnter(object sender, DragEventArgs e) => e.Effect = e.Data.GetDataPresent(DataFormats.FileDrop) ? DragDropEffects.All : DragDropEffects.None;
        #endregion
    }
}
