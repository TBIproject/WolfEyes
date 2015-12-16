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
    public partial class FrmAlgorithmSelection : Form
    {

        bool editing = false;

        public FrmAlgorithmSelection(bool editing)
        {
            InitializeComponent();
            this.editing = editing;
            if (editing)
            {
                btnCancel.Text = "Apply";
                btnNext.Enabled = false;
            }
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.SelectCamera);
            Close();
        }

        private void FrmMode_FormClosing(object sender, FormClosingEventArgs e)
        {
            
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset.DetectionMethod = Preset.DetectionMethodEnum.ByReference;
            if(!editing) ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.CameraSettings);
            Close();
        }

        private void btnByColor_Click(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset.DetectionMethod = Preset.DetectionMethodEnum.ByColor;
            if (!editing) ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.CameraSettings);
            Close();
        }

        private void btnHybrid_Click(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset.DetectionMethod = Preset.DetectionMethodEnum.Hybrid;
            if (!editing) ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.CameraSettings);
            Close();
        }

        private void FrmMode_Load(object sender, EventArgs e)
        {

        }
    }
}
