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
    public partial class FrmMode : Form
    {
        public FrmMode()
        {
            InitializeComponent();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            ApplicationData.wizardStep = ApplicationData.WizardStep.SelectCamera;
            Close();
        }

        private void FrmMode_FormClosing(object sender, FormClosingEventArgs e)
        {
            
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ApplicationData.detectionMethod = Camera.DetectionMethod.ByReference;
            ApplicationData.wizardStep = ApplicationData.WizardStep.CameraSettings;
            Close();
        }

        private void btnByColor_Click(object sender, EventArgs e)
        {
            ApplicationData.detectionMethod = Camera.DetectionMethod.ByColor;
            ApplicationData.wizardStep = ApplicationData.WizardStep.CameraSettings;
            Close();
        }

        private void btnHybrid_Click(object sender, EventArgs e)
        {
            ApplicationData.detectionMethod = Camera.DetectionMethod.Hybrid;
            ApplicationData.wizardStep = ApplicationData.WizardStep.CameraSettings;
            Close();
        }

        private void FrmMode_Load(object sender, EventArgs e)
        {

        }
    }
}
