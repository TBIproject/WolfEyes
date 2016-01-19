using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WolfEyes
{
    public partial class FrmDeviceSelection : Form
    {
        public FrmDeviceSelection(bool editing)
        {
            InitializeComponent();
            if(editing)
            {
                btnNext.Enabled = false;
                btnPrevious.Enabled = false;
                btnCancel.Text = "Apply";
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void FrmSelectCamera_Load(object sender, EventArgs e)
        {
            if(ApplicationData.selectedPreset.Devices.Count == 2)
            {
                nudDevice1.Value = ApplicationData.selectedPreset.Devices[0].ID;
                nudDevice2.Value = ApplicationData.selectedPreset.Devices[1].ID;
            }
            UpdateEngine();
        }

        private void btnUpdate_Click(object sender, EventArgs e)
        {
            Enabled = false;
            Engine.StopEngine(() =>
            {
                UpdateEngine();
                Invoke(new MethodInvoker(() => Enabled = true));
            });
        }

        private void UpdateEngine()
        {
            ApplicationData.selectedPreset.DeleteAllDevices();
            ApplicationData.selectedPreset.RegisterDevice((int)nudDevice1.Value);
            //ApplicationData.selectedPreset.RegisterDevice((int)nudDevice2.Value);
            Engine.SetCameraOutput(0, Preset.DetectionMethodEnum.None, picDevice1, true);
            //Engine.SetCameraOutput(1, Preset.DetectionMethodEnum.None, picDevice2);
            Engine.StartEngine();
        }

        private void FrmSelectCamera_FormClosing(object sender, FormClosingEventArgs e)
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

        private void btnNext_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.SelectMode);
            Close();
        }

        private void btnPrevious_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.PresetName);
            Close();
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
