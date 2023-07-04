using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace BuildTTC
{
    public partial class BuildTTC : Form
    {
        readonly OpenFileDialog openFileDialog = new OpenFileDialog();
        readonly SaveFileDialog saveFileDialog = new SaveFileDialog();
        string exefl;
        private string args;
        private System.Threading.Thread thRun;
        private string err;
        private string outinfo;
        public BuildTTC()
        {
            InitializeComponent();
            buttonAdd.Click += ButtonAdd_Click;
            buttonRemove.Click += ButtonRemove_Click;
            buttonInsert.Click += ButtonInsert_Click;
            buttonUp.Click += ButtonUp_Click;
            buttonDown.Click += ButtonDown_Click;
            buttonClear.Click += ButtonClear_Click;
            listBox.DragEnter += ListBox_DragEnter;
            listBox.DragDrop += ListBox_DragDrop;
            button1.Click += Button1_Click;
            buttonOK.Click += ButtonOK_Click;
            openFileDialog.Multiselect = true;
            openFileDialog.Filter = "字体文件|*.ttf;*.otf|所有文件|*";
        }

        private void ButtonOK_Click(object sender, EventArgs e)
        {
            if (listBox.Items.Count < 2)
            {
                MessageBox.Show(this, "字体文件太少，请添加字体！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }
            if (string.IsNullOrWhiteSpace(textBox1.Text))
            {
                MessageBox.Show(this, "请选择保存文件！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }
            bool isgetexe = false;
            string path = AppDomain.CurrentDomain.BaseDirectory;
            args = "";
            if (System.IO.File.Exists(path + "python/python.exe") && System.IO.File.Exists(path + "otf2otc.py"))
            {
                exefl = path + "python/python.exe";
                args += " \"" + path + "otf2otc.py\"";
                isgetexe = true;
            }
            else if (IsInPATH("python.exe") && System.IO.File.Exists(path + "otf2otc.py"))
            {
                exefl = "python";
                args += " \"" + path + "otf2otc.py\"";
                isgetexe = true;
            }
            else if (IsInPATH("otf2otc.exe"))
            {
                exefl = "otf2otc";
                isgetexe = true;
            }
            if (!isgetexe)
            {
                MessageBox.Show(this, "未找到 otf2otc 程序！", "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }
            args += $" -o \"{textBox1.Text}\"";
            foreach (var item in listBox.Items)
            {
                args += " \"" + item + "\"";
            }
            tableLayoutPanel1.Enabled = false;
            Cursor = Cursors.WaitCursor;
            err = "";
            outinfo = "";
            thRun = new System.Threading.Thread(ThRun);
            thRun.IsBackground = true;
            thRun.Start();
        }

        private void ThRun()
        {
            using (System.Diagnostics.Process p = new System.Diagnostics.Process())
            {
                p.StartInfo.FileName = exefl;
                p.StartInfo.Arguments = args;
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = true;
                p.StartInfo.RedirectStandardError = true;
                p.StartInfo.RedirectStandardOutput = true;
                p.Start();
                p.ErrorDataReceived += P_ErrorDataReceived;
                p.OutputDataReceived += P_OutputDataReceived;
                p.BeginErrorReadLine();
                p.BeginOutputReadLine();
                p.WaitForExit();
                p.Close();
            }
            Invoke(new Action(delegate
            {
                tableLayoutPanel1.Enabled = true;
                Cursor = Cursors.Default;
                if (string.IsNullOrWhiteSpace(err))
                {
                    MessageBox.Show(this, "处理完毕！\r\n" + outinfo, "提示", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show(this, "出现错误！\r\n" + err, "提示", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }));
        }
        private void P_OutputDataReceived(object sender, System.Diagnostics.DataReceivedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(e.Data))
            {
                outinfo += e.Data + "\r\n";
            }
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

        private void Button1_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "字体文件|*.ttc;*.otc|所有文件|*";
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                textBox1.Text = saveFileDialog.FileName;
            }
        }

        #region Button
        private void ButtonAdd_Click(object sender, EventArgs e) => AddfileToList();
        private void ButtonRemove_Click(object sender, EventArgs e) => RemoveSelected();
        private void ButtonUp_Click(object sender, EventArgs e) => UpfileToList();
        private void ButtonDown_Click(object sender, EventArgs e) => DownfileToList();
        private void ButtonInsert_Click(object sender, EventArgs e) => InsertfileToList();
        private void ButtonClear_Click(object sender, EventArgs e) => listBox.Items.Clear();

        #endregion

        #region ListView

        private void ListBox_DragDrop(object sender, DragEventArgs e)
        {
            Array file = (System.Array)e.Data.GetData(DataFormats.FileDrop);
            foreach (var item in file)
            {
                if (System.IO.File.Exists((string)item))
                {
                    listBox.Items.Add((string)item);
                }
            }
        }

        private void ListBox_DragEnter(object sender, DragEventArgs e) => e.Effect = e.Data.GetDataPresent(DataFormats.FileDrop) ? DragDropEffects.All : DragDropEffects.None;

        #endregion

        #region Main


        private void AddfileToList()
        {
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                foreach (var item in openFileDialog.FileNames)
                {
                    listBox.Items.Add(item);
                }
            }
        }
        private void UpfileToList()
        {
            int i = listBox.SelectedIndex;
            if (i < 0)
            {
                return;
            }
            if (i > 0)
            {
                var item = listBox.Items[i - 1];
                listBox.Items[i - 1] = listBox.Items[i];
                listBox.Items[i] = item;
                listBox.SelectedIndex = i - 1;
            }

        }
        private void DownfileToList()
        {
            int i = listBox.SelectedIndex;
            if (i < 0)
            {
                return;
            }
            if (i < listBox.Items.Count - 1)
            {
                var item = listBox.Items[i];
                listBox.Items[i] = listBox.Items[i + 1];
                listBox.Items[i + 1] = item;
                listBox.SelectedIndex = i + 1;
            }

        }
        private void InsertfileToList()
        {
            int i = listBox.SelectedIndex;
            if (i < 0)
            {
                return;
            }
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                listBox.Items.Insert(i, openFileDialog.FileName);
            }

        }

        private void RemoveSelected()
        {
            int index = listBox.SelectedIndex;
            if (index < 0)
            {
                return;
            }
            listBox.Items.RemoveAt(index);
            if (index >= listBox.Items.Count - 1 && index > 0)
            {
                listBox.SelectedIndex = listBox.Items.Count - 1;
            }
            else if (index == 0 && listBox.Items.Count > 0)
            {
                listBox.SelectedIndex = 0;
            }
            else
            {
                listBox.SelectedIndex = index - 1;
            }
        }

        #endregion
        private void TextBox_DragEnter(object sender, DragEventArgs e) => e.Effect = e.Data.GetDataPresent(DataFormats.FileDrop) ? DragDropEffects.All : DragDropEffects.None;
        private void TextBox_DragDrop(object sender, DragEventArgs e) => ((TextBox)sender).Text = ((System.Array)e.Data.GetData(DataFormats.FileDrop)).GetValue(0).ToString();

    }
}
