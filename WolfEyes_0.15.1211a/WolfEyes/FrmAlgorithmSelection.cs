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
        public FrmAlgorithmSelection()
        {
            InitializeComponent();
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
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.CameraSettings);
            Close();
        }

        private void btnByColor_Click(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset.DetectionMethod = Preset.DetectionMethodEnum.ByColor;
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.CameraSettings);
            Close();
        }

        private void btnHybrid_Click(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset.DetectionMethod = Preset.DetectionMethodEnum.Hybrid;
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.CameraSettings);
            Close();
        }

        private void FrmMode_Load(object sender, EventArgs e)
        {

        }
    }
}
