using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WolfEyes
{
    class Wizard
    {
        public enum WizardStepEnum
        {
            SelectCamera,
            SelectMode,
            CameraSettings,
            Calibration,
            PresetName,
            None
        }

        private WizardStepEnum wizardStep;
        public WizardStepEnum WizardStep
        {
            get { return wizardStep; }
            set { wizardStep = value; }
        }

        public Wizard(WizardStepEnum wizardStep)
        {
            this.wizardStep = wizardStep;
        }

        public void Show(bool editing = false)
        {
            WizardStepEnum previous = WizardStepEnum.None;

            while (WizardStep != previous)
            {
                previous = WizardStep;

                switch (WizardStep)
                {
                    case WizardStepEnum.SelectCamera:
                        new FrmDeviceSelection(editing).ShowDialog();
                        break;

                    case WizardStepEnum.SelectMode:
                        new FrmAlgorithmSelection(editing).ShowDialog();
                        break;

                    case WizardStepEnum.CameraSettings:
                        new FrmDeviceSettings(editing).ShowDialog();
                        break;

                    case WizardStepEnum.Calibration:
                        new FrmCalibration(editing).ShowDialog();
                        break;

                    case WizardStepEnum.PresetName:
                        new FrmPresetName(editing).ShowDialog();
                        break;
                }
            }
        }

        public void SetNextStep(WizardStepEnum wizardStep)
        {
            this.WizardStep = wizardStep;
        }
    }
}
