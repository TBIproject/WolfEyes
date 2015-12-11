using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Gma.System.MouseKeyHook;

namespace WolfEyes
{
    public partial class FrmDeviceSettings : Form
    {
        IKeyboardMouseEvents hook;

        public FrmDeviceSettings()
        {
            InitializeComponent();
            hook = Hook.GlobalEvents();
            hook.KeyDown += Hook_KeyDown;
        }

        private void FrmCameraSettings_Load(object sender, EventArgs e)
        {
            //nudBandBottom.Value = Convert.ToInt32(ApplicationData.selectedPreset.BandMin * 100);
            //nudBandTop.Value = Convert.ToInt32(ApplicationData.selectedPreset.BandMax * 100);
            nudBlur.Value = ApplicationData.selectedPreset.Blur;
            nudByColorDilate.Value = ApplicationData.selectedPreset.Dilate;
            nudByColorThresh.Value = ApplicationData.selectedPreset.Threshold;
            nudByRefThresh.Value = ApplicationData.selectedPreset.ThresholdDiff;
            nudExposure.Value = ApplicationData.selectedPreset.Exposure;
            nudHueHighMin.Value = ApplicationData.selectedPreset.HueHighMin;
            nudHueLowMax.Value = ApplicationData.selectedPreset.HueLowMax;
            nudHueLowMin.Value = ApplicationData.selectedPreset.HueLowMin;
            nudMinSize.Value = ApplicationData.selectedPreset.MinSize;
            nudOffshore.Value = ApplicationData.selectedPreset.Offshore;

            lblBandBottom.Text = ApplicationData.selectedPreset.BandMin.ToString();
            lblBandTop.Text = ApplicationData.selectedPreset.BandMax.ToString();
            lblBlur.Text = ApplicationData.selectedPreset.Blur.ToString();
            lblByColorDilate.Text = ApplicationData.selectedPreset.Dilate.ToString();
            lblByColorThresh.Text = ApplicationData.selectedPreset.Threshold.ToString();
            lblByRefThresh.Text = ApplicationData.selectedPreset.ThresholdDiff.ToString();
            lblExposure.Text = ApplicationData.selectedPreset.Exposure.ToString();
            lblHueHighMin.Text = ApplicationData.selectedPreset.HueHighMin.ToString();
            lblHueLowMax.Text = ApplicationData.selectedPreset.HueLowMax.ToString();
            lblHueLowMin.Text = ApplicationData.selectedPreset.HueLowMin.ToString();
            lblMinSize.Text = ApplicationData.selectedPreset.MinSize.ToString();
            lblOffshore.Text = ApplicationData.selectedPreset.Offshore.ToString();

            UpdateEngine();
        }

        private void Hook_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.KeyCode == Keys.F1)
            {
                foreach (Camera device in ApplicationData.selectedPreset.Devices)
                    new Task(() => device.CumulativeReference(10)).Start();
            }
        }

        private void UpdateEngine()
        {
            Engine.SetCameraOutput(0, ApplicationData.selectedPreset.DetectionMethod, picDevice1, true);
            Engine.SetCameraOutput(1, ApplicationData.selectedPreset.DetectionMethod, picDevice2);
            Engine.StartEngine();
        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.Calibration);
            Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            ApplicationData.wizard.SetNextStep(Wizard.WizardStepEnum.SelectMode);
            Close();
        }

        private void nudHueLowMin_Scroll(object sender, EventArgs e)
        {
            lblHueLowMin.Text = nudHueLowMin.Value.ToString();
            ApplicationData.selectedPreset.HueLowMin = nudHueLowMin.Value;
        }

        private void nudHueLowMax_Scroll(object sender, EventArgs e)
        {
            lblHueLowMax.Text = nudHueLowMax.Value.ToString();
            ApplicationData.selectedPreset.HueLowMax = nudHueLowMax.Value;
        }

        private void nudHueHighMin_Scroll(object sender, EventArgs e)
        {
            lblHueHighMin.Text = nudHueHighMin.Value.ToString();
            ApplicationData.selectedPreset.HueHighMin = nudHueHighMin.Value;
        }

        private void nudBlur_Scroll(object sender, EventArgs e)
        {
            lblBlur.Text = nudBlur.Value.ToString();
            ApplicationData.selectedPreset.Blur = nudBlur.Value;
        }

        private void nudExposure_Scroll(object sender, EventArgs e)
        {
            lblExposure.Text = nudExposure.Value.ToString();
            ApplicationData.selectedPreset.Exposure = nudExposure.Value;
        }

        private void nudMinSize_Scroll(object sender, EventArgs e)
        {
            lblMinSize.Text = nudMinSize.Value.ToString();
            ApplicationData.selectedPreset.MinSize = nudMinSize.Value;
        }

        private void nudOffshore_Scroll(object sender, EventArgs e)
        {
            lblOffshore.Text = nudOffshore.Value.ToString();
            ApplicationData.selectedPreset.Offshore = nudOffshore.Value;
        }

        private void nudByColorThresh_Scroll(object sender, EventArgs e)
        {
            lblByColorThresh.Text = nudByColorThresh.Value.ToString();
            ApplicationData.selectedPreset.Threshold = nudByColorThresh.Value;
        }

        private void nudByRefThresh_Scroll(object sender, EventArgs e)
        {
            lblByRefThresh.Text = nudByRefThresh.Value.ToString();
            ApplicationData.selectedPreset.ThresholdDiff = nudByRefThresh.Value;
        }

        private void nudByColorDilate_Scroll(object sender, EventArgs e)
        {
            lblByColorDilate.Text = nudByColorDilate.Value.ToString();
            ApplicationData.selectedPreset.Dilate = nudByColorDilate.Value;
        }

        private void nudBandTop_Scroll(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset.BandMin = nudBandTop.Value / 100.0;
            lblBandTop.Text = ApplicationData.selectedPreset.BandMin.ToString();
        }

        private void nudBandBottom_Scroll(object sender, EventArgs e)
        {
            ApplicationData.selectedPreset.BandMax = nudBandBottom.Value / 100.0;
            lblBandBottom.Text = ApplicationData.selectedPreset.BandMax.ToString();
        }

        private void FrmCameraSettings_FormClosing(object sender, FormClosingEventArgs e)
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
    }
}
