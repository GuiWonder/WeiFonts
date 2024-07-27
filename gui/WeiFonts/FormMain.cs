using System;
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
        private string exepy;
        private readonly string path;
        private string err;
        private string args;
        private System.Threading.Thread thRun;

        public FormMain()
        {
            InitializeComponent();
            path = AppDomain.CurrentDomain.BaseDirectory;
            linkLabelWeb.LinkClicked += LinkLabelWeb_LinkClicked;
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
        }


        private void ButtonStartPf_Click(object sender, System.EventArgs e)
        {
            string fileout = textBoxOutPf.Text.Trim();
            string[] infls = { textBox1.Text, textBox2.Text, textBox3.Text, textBox4.Text, textBox5.Text, textBox6.Text };
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

            string pyfile = path + "files/weipingfang.py";
            pyfile = pyfile.Replace('\\', '/');
            args = $"\"{pyfile}\" -o \"{fileout}\"";
            for (int i = 0; i < infls.Length; i++)
            {
                args += $" -f{i + 1} \"{infls[i]}\"";
            }
            RunArgs();
        }

        private void NoFileErr(string item) => MessageBox.Show(this, $"文件{item}无效，请重新选择。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
        private void SellFileInfo() => MessageBox.Show(this, "请选择保存文件。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
        private void NoPYErr() => MessageBox.Show(this, "未能找到 Python。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);

        private void ButtonStartWin_Click(object sender, System.EventArgs e)
        {
            string filein = textBoxInWin.Text.Trim();
            string dirout = textBoxOutWin.Text.Trim();
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
                SellFileInfo();
                return;
            }

            string[] tgs = { "msyh", "msjh", "mingliu", "simsun", "simhei", "msgothic", "msmincho", "meiryo", "malgun", "yugoth", "yumin", "batang", "gulim", "allsans", "allserif", "all", "mingliub", "simsunb" };
            string tg = tgs[comboBoxMBWin.SelectedIndex];
            string pyfile = path + "files/weiwin.py";
            pyfile = pyfile.Replace('\\', '/');
            args = $"\"{pyfile}\" -i \"{filein}\" -d \"{dirout}\" -tg {tg}";
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
            RunArgs();
        }

        private void ButtonStartWei_Click(object sender, System.EventArgs e)
        {
            string filein = textBoxInWei.Text.Trim();
            string fileout = textBoxOutWei.Text.Trim();
            string filem = textBoxM.Text.Trim();
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

            string pyfile = path + "files/weiwei.py";
            pyfile = pyfile.Replace('\\', '/');
            args = $"\"{pyfile}\" -i \"{filein}\" -o \"{fileout}\" -m \"{filem}\"";
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
            err = "";
            thRun = new System.Threading.Thread(ThRun)
            {
                IsBackground = true
            };
            thRun.Start();
        }

        private void ThRun()
        {
            using (System.Diagnostics.Process p = new System.Diagnostics.Process())
            {
                p.StartInfo.FileName = exepy;
                p.StartInfo.Arguments = args;
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = true;
                p.StartInfo.RedirectStandardError = true;
                p.Start();
                p.ErrorDataReceived += P_ErrorDataReceived;
                p.BeginErrorReadLine();
                p.WaitForExit();
                p.Close();
            }
            Invoke(new Action(delegate
            {
                tabControl1.Enabled = true;
                Cursor = Cursors.Default;
                if (string.IsNullOrWhiteSpace(err))
                {
                    MessageBox.Show(this, "处理完毕！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show(this, "出现错误！\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }));
        }

        private void P_ErrorDataReceived(object sender, System.Diagnostics.DataReceivedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(e.Data))
            {
                err += e.Data + "\r\n";
            }
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
                if (textBoxM.Text.ToLower().Trim().EndsWith("ttc"))
                {
                    saveFileDialog.Filter = "字体文件|*.ttc;*.ttf;*.otf;*.otc|所有文件|*.*";
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

        private void LinkLabelWeb_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            System.Diagnostics.Process.Start("https://github.com/GuiWonder/WeiFonts");
        }
        #endregion
    }
}
