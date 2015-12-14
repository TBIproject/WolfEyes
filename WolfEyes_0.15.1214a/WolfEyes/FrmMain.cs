using Gma.System.MouseKeyHook;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WolfEyes
{
    public partial class FrmMain : Form
    {
        IKeyboardMouseEvents hook;
        bool down = false;

        [DllImport("user32.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
        public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, uint dwExtraInfo);

        private const int MOUSEEVENTF_LEFTDOWN = 0x02;
        private const int MOUSEEVENTF_LEFTUP = 0x04;
        private const int MOUSEEVENTF_RIGHTDOWN = 0x08;
        private const int MOUSEEVENTF_RIGHTUP = 0x10;

        public FrmMain()
        {
            InitializeComponent();
            hook = Hook.GlobalEvents();
            hook.KeyDown += Hook_KeyDown;
            hook.KeyUp += hook_KeyUp;
        }

        void hook_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Insert)
            {
                if (down)
                {
                    down = false;
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                }
            }
        }

        private void Hook_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.F2)
            {
                ToggleEngine();
            }

            if(e.KeyCode == Keys.Insert)
            {
                if (!down)
                {
                    down = true;
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                }
            }
        }

        private void btnWizard_Click(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset = new Preset();
            ApplicationData.wizard = new Wizard(Wizard.WizardStepEnum.PresetName);
            ApplicationData.wizard.Show();
            if (ApplicationData.wizard.WizardStep != Wizard.WizardStepEnum.Calibration)
            {
                if (cbxPresets.SelectedItem != null && ApplicationData.presets.ContainsKey(cbxPresets.SelectedItem.ToString()))
                {
                    ApplicationData.selectedPreset = ApplicationData.presets[cbxPresets.SelectedItem.ToString()];
                }
                else
                {
                    ApplicationData.selectedPreset = null;
                }
            }
            else
            {
                ApplicationData.presets.Add(ApplicationData.selectedPreset.Name, ApplicationData.selectedPreset);
                UpdatePresetList();
                cbxPresets.SelectedItem = ApplicationData.selectedPreset.Name;
            }
        }

        private void UpdatePresetList()
        {
            cbxPresets.Items.Clear();
            foreach (KeyValuePair<string, Preset> entry in ApplicationData.presets)
                cbxPresets.Items.Add(entry.Key);
        }

        private void UpdateEngine()
        {
            Engine.EnableMouseControl();
            Engine.ReadCamera(0, ApplicationData.selectedPreset.DetectionMethod, true);
            Engine.ReadCamera(1, ApplicationData.selectedPreset.DetectionMethod);
            Engine.StartEngine();
        }

        private void startCaptureToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ToggleEngine();
        }

        private void ToggleEngine()
        {
            if (!Engine.Running)
            {
                if (ApplicationData.selectedPreset != null)
                {
                    UpdateEngine();
                    startCaptureToolStripMenuItem.Text = "Stop whiteboard engine";
                    lblEngine.Text = "running";
                }
                else
                    MessageBox.Show("No preset loaded ! Please use the preset wizard.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else
            {
                Enabled = false;

                Engine.StopEngine(() =>
                {
                    Invoke(new MethodInvoker(() => {
                        Enabled = true;
                        startCaptureToolStripMenuItem.Text = "Start whiteboard engine";
                        lblEngine.Text = "stopped";
                    }));
                });
            }
        }

        private void FrmMain_Load(object sender, EventArgs e)
        {

        }

        private void btnAdvanced1_Click(object sender, EventArgs e)
        {

        }

        private void FrmMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (Engine.Running)
            {
                e.Cancel = true;

                Engine.StopEngine(() =>
                {
                    Invoke(new MethodInvoker(() => Close()));
                });
            }
        }

        private void btnDeviceSelection_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard = new Wizard(Wizard.WizardStepEnum.SelectCamera);
            ApplicationData.wizard.Show(true);
        }

        private void btnAlgorithmSelection_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard = new Wizard(Wizard.WizardStepEnum.SelectMode);
            ApplicationData.wizard.Show(true);
        }

        private void btnDeviceSettings_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard = new Wizard(Wizard.WizardStepEnum.CameraSettings);
            ApplicationData.wizard.Show(true);
        }

        private void btnCalibrate_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard = new Wizard(Wizard.WizardStepEnum.Calibration);
            ApplicationData.wizard.Show(true);
        }

        private void tabControl1_Selecting(object sender, TabControlCancelEventArgs e)
        {
            lblPresetWarning.Visible = (ApplicationData.selectedPreset == null);
            btnAlgorithmSelection.Enabled = (ApplicationData.selectedPreset != null);
            btnPresetName.Enabled = (ApplicationData.selectedPreset != null);
            btnCalibrate.Enabled = (ApplicationData.selectedPreset != null);
            btnDeviceSelection.Enabled = (ApplicationData.selectedPreset != null);
            btnDeviceSettings.Enabled = (ApplicationData.selectedPreset != null);
        }

        private void tabPage1_Click(object sender, EventArgs e)
        {

        }

        private void btnPresetName_Click(object sender, EventArgs e)
        {
            string oldName = ApplicationData.selectedPreset.Name;

            ApplicationData.wizard = new Wizard(Wizard.WizardStepEnum.PresetName);
            ApplicationData.wizard.Show(true);

            ApplicationData.presets.Remove(oldName);
            ApplicationData.presets.Add(ApplicationData.selectedPreset.Name, ApplicationData.selectedPreset);
            UpdatePresetList();
            cbxPresets.SelectedItem = ApplicationData.selectedPreset.Name;
        }

        private void cbxPresets_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (Engine.Running)
            {
                Enabled = false;

                Engine.StopEngine(() =>
                {
                    Enabled = true;
                    Invoke(new MethodInvoker(() =>
                    {
                        startCaptureToolStripMenuItem.Text = "Start whiteboard engine";
                        lblEngine.Text = "stopped";
                    }));
                });
            }

            if (ApplicationData.presets.ContainsKey(cbxPresets.SelectedItem.ToString()))
                ApplicationData.selectedPreset = ApplicationData.presets[cbxPresets.SelectedItem.ToString()];
        }

        private void loadPresetToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (ApplicationData.selectedPreset != null)
            {
                if (ApplicationData.selectedPreset.FileName != "")
                {
                    ApplicationData.SavePreset(ApplicationData.selectedPreset.FileName);
                }
                else
                {
                    saveFileDialog1.FileName = ApplicationData.selectedPreset.Name;
                    saveFileDialog1.ShowDialog();
                }
            }
            else
                MessageBox.Show("No preset to save !", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            openFileDialog1.ShowDialog();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (cbxPresets.SelectedItem != null)
            {
                saveFileDialog1.FileName = ApplicationData.selectedPreset.Name;
                saveFileDialog1.ShowDialog();
            }
            else
                MessageBox.Show("No preset to save !", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void saveFileDialog1_FileOk(object sender, CancelEventArgs e)
        {
            ApplicationData.SavePreset(saveFileDialog1.FileName);
        }

        private void openFileDialog1_FileOk(object sender, CancelEventArgs e)
        {
            ApplicationData.LoadPreset(openFileDialog1.FileName);

            ApplicationData.wizard = new Wizard(Wizard.WizardStepEnum.Calibration);
            ApplicationData.wizard.Show();
            if (ApplicationData.wizard.WizardStep != Wizard.WizardStepEnum.Calibration)
            {
                if (cbxPresets.SelectedItem != null && ApplicationData.presets.ContainsKey(cbxPresets.SelectedItem.ToString()))
                {
                    ApplicationData.selectedPreset = ApplicationData.presets[cbxPresets.SelectedItem.ToString()];
                }
                else
                {
                    ApplicationData.selectedPreset = null;
                }
            }
            else
            {
                ApplicationData.presets.Add(ApplicationData.selectedPreset.Name, ApplicationData.selectedPreset);
                UpdatePresetList();
                cbxPresets.SelectedItem = ApplicationData.selectedPreset.Name;
            }
        }
    }
}
