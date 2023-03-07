using System;
using System.IO;
using System.Windows.Forms;

namespace toWinFonts
{
    public partial class FormMain : Form
    {
        public FormMain()
        {
            InitializeComponent();
        }

        private string exepy;
        private string path;
        private string args;
        private System.Threading.Thread thRun;
        private string err;

        private void FormMain_Load(object sender, EventArgs e)
        {
            CheckForIllegalCrossThreadCalls = false;
            comboBox1.SelectedIndex = 0;
            comboBox2.SelectedIndex = 0;
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
        private void ButtonStart_Click(object sender, EventArgs e)
        {
            path = AppDomain.CurrentDomain.BaseDirectory;
            string filein = textBoxIn.Text.Trim();
            string dirout = textBoxOut.Text.Trim();
            exepy = path + "python/python.exe";
            if (!System.IO.File.Exists(exepy))
            {
                if (IsInPATH("python.exe"))
                {
                    exepy = "python";
                }
                else
                {
                    MessageBox.Show(this, "未能找到 Python。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
            }
            if (!System.IO.File.Exists(filein))
            {
                MessageBox.Show(this, "文件无效，请重新选择。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (!System.IO.Directory.Exists(dirout))
            {
                MessageBox.Show(this, "保存目录不存在，请重新选择。", "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            string tg = "";
            switch (comboBox1.SelectedIndex)
            {
                case 0:
                    tg = "msyh";
                    break;
                case 1:
                    tg = "msjh";
                    break;
                case 2:
                    tg = "mingliu";
                    break;
                case 3:
                    tg = "simsun";
                    break;
                case 4:
                    tg = "yugoth";
                    break;
                case 5:
                    tg = "msgothic";
                    break;
                case 6:
                    tg = "malgun";
                    break;
                case 7:
                    tg = "msmincho";
                    break;
                case 8:
                    tg = "meiryo";
                    break;
                case 9:
                    tg = "batang";
                    break;
                default:
                    break;
            }

            string pyfile = path + "winfont.py";

            pyfile = pyfile.Replace('\\', '/');
            args = $"\"{pyfile}\" -i \"{filein}\" -d \"{dirout}\" -tg {tg}";
            if (comboBox2.SelectedIndex != 0)
            {
                args += $" -wt {comboBox2.Text}";
            }
            panelMain.Enabled = false;
            Cursor = Cursors.WaitCursor;
            err = "";
            thRun = new System.Threading.Thread(ThRun);
            thRun.IsBackground = true;
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
                panelMain.Enabled = true;
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

        private void FormMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (thRun != null && thRun.IsAlive)
            {
                e.Cancel = true;
            }
        }
        private void TextBox_DragEnter(object sender, DragEventArgs e) => e.Effect = e.Data.GetDataPresent(DataFormats.FileDrop) ? DragDropEffects.All : DragDropEffects.None;
        private void TextBox_DragDrop(object sender, DragEventArgs e) => ((TextBox)sender).Text = ((System.Array)e.Data.GetData(DataFormats.FileDrop)).GetValue(0).ToString();

        private void LinkLabelIn_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                textBoxIn.Text = openFileDialog1.FileName;
            }
        }

        private void LinkLabelOut_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            if (folderBrowserDialog1.ShowDialog() == DialogResult.OK)
            {
                textBoxOut.Text = folderBrowserDialog1.SelectedPath;
            }
        }

        private void LinkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            System.Diagnostics.Process.Start("https://github.com/GuiWonder/toWinFonts");
        }
    }
}
