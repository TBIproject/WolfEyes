namespace WolfEyes
{
    partial class FrmWizard
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.btnDone = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.lblO = new System.Windows.Forms.Label();
            this.lblI = new System.Windows.Forms.Label();
            this.lblJ = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.lblMousePos = new System.Windows.Forms.Label();
            this.panel1 = new System.Windows.Forms.Panel();
            this.btnPrevious = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            this.picDevice2 = new System.Windows.Forms.PictureBox();
            this.picDevice1 = new System.Windows.Forms.PictureBox();
            this.label11 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.lblInfo = new System.Windows.Forms.Label();
            this.lblO2 = new System.Windows.Forms.Label();
            this.lblJ2 = new System.Windows.Forms.Label();
            this.lblI2 = new System.Windows.Forms.Label();
            this.picPointJ = new System.Windows.Forms.Panel();
            this.nudOffset = new System.Windows.Forms.NumericUpDown();
            this.label5 = new System.Windows.Forms.Label();
            this.picPointO = new System.Windows.Forms.Panel();
            this.picPointI = new System.Windows.Forms.Panel();
            this.picPointITemp = new System.Windows.Forms.Panel();
            this.panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.picDevice2)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.picDevice1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.nudOffset)).BeginInit();
            this.SuspendLayout();
            // 
            // btnDone
            // 
            this.btnDone.Location = new System.Drawing.Point(346, 269);
            this.btnDone.Name = "btnDone";
            this.btnDone.Size = new System.Drawing.Size(75, 23);
            this.btnDone.TabIndex = 0;
            this.btnDone.Text = "Finish";
            this.btnDone.UseVisualStyleBackColor = true;
            this.btnDone.Click += new System.EventHandler(this.btnDone_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 6);
            this.label1.Margin = new System.Windows.Forms.Padding(5);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(36, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "1 - O :";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 29);
            this.label2.Margin = new System.Windows.Forms.Padding(5);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(31, 13);
            this.label2.TabIndex = 1;
            this.label2.Text = "1 - I :";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 52);
            this.label3.Margin = new System.Windows.Forms.Padding(5);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(33, 13);
            this.label3.TabIndex = 1;
            this.label3.Text = "1 - J :";
            // 
            // lblO
            // 
            this.lblO.AutoSize = true;
            this.lblO.Location = new System.Drawing.Point(58, 6);
            this.lblO.Margin = new System.Windows.Forms.Padding(5);
            this.lblO.Name = "lblO";
            this.lblO.Size = new System.Drawing.Size(60, 13);
            this.lblO.TabIndex = 1;
            this.lblO.Text = "not defined";
            // 
            // lblI
            // 
            this.lblI.AutoSize = true;
            this.lblI.Location = new System.Drawing.Point(58, 29);
            this.lblI.Margin = new System.Windows.Forms.Padding(5);
            this.lblI.Name = "lblI";
            this.lblI.Size = new System.Drawing.Size(60, 13);
            this.lblI.TabIndex = 1;
            this.lblI.Text = "not defined";
            // 
            // lblJ
            // 
            this.lblJ.AutoSize = true;
            this.lblJ.Location = new System.Drawing.Point(58, 52);
            this.lblJ.Margin = new System.Windows.Forms.Padding(5);
            this.lblJ.Name = "lblJ";
            this.lblJ.Size = new System.Drawing.Size(60, 13);
            this.lblJ.TabIndex = 1;
            this.lblJ.Text = "not defined";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(12, 95);
            this.label7.Margin = new System.Windows.Forms.Padding(5);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(84, 13);
            this.label7.TabIndex = 1;
            this.label7.Text = "Mouse position :";
            // 
            // lblMousePos
            // 
            this.lblMousePos.AutoSize = true;
            this.lblMousePos.Location = new System.Drawing.Point(106, 95);
            this.lblMousePos.Margin = new System.Windows.Forms.Padding(5);
            this.lblMousePos.Name = "lblMousePos";
            this.lblMousePos.Size = new System.Drawing.Size(51, 13);
            this.lblMousePos.TabIndex = 1;
            this.lblMousePos.Text = "unknown";
            // 
            // panel1
            // 
            this.panel1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.panel1.BackColor = System.Drawing.SystemColors.Control;
            this.panel1.Controls.Add(this.label5);
            this.panel1.Controls.Add(this.nudOffset);
            this.panel1.Controls.Add(this.btnPrevious);
            this.panel1.Controls.Add(this.btnCancel);
            this.panel1.Controls.Add(this.label4);
            this.panel1.Controls.Add(this.picDevice2);
            this.panel1.Controls.Add(this.picDevice1);
            this.panel1.Controls.Add(this.label11);
            this.panel1.Controls.Add(this.label10);
            this.panel1.Controls.Add(this.label1);
            this.panel1.Controls.Add(this.label3);
            this.panel1.Controls.Add(this.label9);
            this.panel1.Controls.Add(this.btnDone);
            this.panel1.Controls.Add(this.label2);
            this.panel1.Controls.Add(this.lblInfo);
            this.panel1.Controls.Add(this.label7);
            this.panel1.Controls.Add(this.lblO2);
            this.panel1.Controls.Add(this.lblMousePos);
            this.panel1.Controls.Add(this.lblJ2);
            this.panel1.Controls.Add(this.lblO);
            this.panel1.Controls.Add(this.lblI2);
            this.panel1.Controls.Add(this.lblJ);
            this.panel1.Controls.Add(this.lblI);
            this.panel1.Location = new System.Drawing.Point(532, 12);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(428, 312);
            this.panel1.TabIndex = 2;
            // 
            // btnPrevious
            // 
            this.btnPrevious.Location = new System.Drawing.Point(265, 269);
            this.btnPrevious.Name = "btnPrevious";
            this.btnPrevious.Size = new System.Drawing.Size(75, 23);
            this.btnPrevious.TabIndex = 10;
            this.btnPrevious.Text = "< Previous";
            this.btnPrevious.UseVisualStyleBackColor = true;
            this.btnPrevious.Click += new System.EventHandler(this.btnPrevious_Click);
            // 
            // btnCancel
            // 
            this.btnCancel.Location = new System.Drawing.Point(184, 269);
            this.btnCancel.Name = "btnCancel";
            this.btnCancel.Size = new System.Drawing.Size(75, 23);
            this.btnCancel.TabIndex = 9;
            this.btnCancel.Text = "Cancel";
            this.btnCancel.UseVisualStyleBackColor = true;
            this.btnCancel.Click += new System.EventHandler(this.btnCancel_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(322, 5);
            this.label4.Margin = new System.Windows.Forms.Padding(5);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(101, 65);
            this.label4.TabIndex = 4;
            this.label4.Text = "F1 = New reference\r\nF5 = O\r\nF6 = I\r\nF7 = J\r\nF9 = Calibrate";
            // 
            // picDevice2
            // 
            this.picDevice2.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.picDevice2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.picDevice2.Location = new System.Drawing.Point(167, 158);
            this.picDevice2.Name = "picDevice2";
            this.picDevice2.Size = new System.Drawing.Size(146, 89);
            this.picDevice2.TabIndex = 2;
            this.picDevice2.TabStop = false;
            // 
            // picDevice1
            // 
            this.picDevice1.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.picDevice1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.picDevice1.Location = new System.Drawing.Point(15, 158);
            this.picDevice1.Name = "picDevice1";
            this.picDevice1.Size = new System.Drawing.Size(146, 89);
            this.picDevice1.TabIndex = 3;
            this.picDevice1.TabStop = false;
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(142, 6);
            this.label11.Margin = new System.Windows.Forms.Padding(5);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(36, 13);
            this.label11.TabIndex = 1;
            this.label11.Text = "2 - O :";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(142, 52);
            this.label10.Margin = new System.Windows.Forms.Padding(5);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(33, 13);
            this.label10.TabIndex = 1;
            this.label10.Text = "2 - J :";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(142, 29);
            this.label9.Margin = new System.Windows.Forms.Padding(5);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(31, 13);
            this.label9.TabIndex = 1;
            this.label9.Text = "2 - I :";
            // 
            // lblInfo
            // 
            this.lblInfo.AutoSize = true;
            this.lblInfo.Location = new System.Drawing.Point(12, 125);
            this.lblInfo.Margin = new System.Windows.Forms.Padding(5);
            this.lblInfo.Name = "lblInfo";
            this.lblInfo.Size = new System.Drawing.Size(73, 13);
            this.lblInfo.TabIndex = 1;
            this.lblInfo.Text = "Not calibrated";
            // 
            // lblO2
            // 
            this.lblO2.AutoSize = true;
            this.lblO2.Location = new System.Drawing.Point(188, 6);
            this.lblO2.Margin = new System.Windows.Forms.Padding(5);
            this.lblO2.Name = "lblO2";
            this.lblO2.Size = new System.Drawing.Size(60, 13);
            this.lblO2.TabIndex = 1;
            this.lblO2.Text = "not defined";
            // 
            // lblJ2
            // 
            this.lblJ2.AutoSize = true;
            this.lblJ2.Location = new System.Drawing.Point(188, 52);
            this.lblJ2.Margin = new System.Windows.Forms.Padding(5);
            this.lblJ2.Name = "lblJ2";
            this.lblJ2.Size = new System.Drawing.Size(60, 13);
            this.lblJ2.TabIndex = 1;
            this.lblJ2.Text = "not defined";
            // 
            // lblI2
            // 
            this.lblI2.AutoSize = true;
            this.lblI2.Location = new System.Drawing.Point(188, 29);
            this.lblI2.Margin = new System.Windows.Forms.Padding(5);
            this.lblI2.Name = "lblI2";
            this.lblI2.Size = new System.Drawing.Size(60, 13);
            this.lblI2.TabIndex = 1;
            this.lblI2.Text = "not defined";
            // 
            // picPointJ
            // 
            this.picPointJ.BackColor = System.Drawing.Color.Red;
            this.picPointJ.Location = new System.Drawing.Point(9, 9);
            this.picPointJ.Margin = new System.Windows.Forms.Padding(0);
            this.picPointJ.Name = "picPointJ";
            this.picPointJ.Size = new System.Drawing.Size(18, 18);
            this.picPointJ.TabIndex = 3;
            // 
            // nudOffset
            // 
            this.nudOffset.Location = new System.Drawing.Point(346, 123);
            this.nudOffset.Maximum = new decimal(new int[] {
            200,
            0,
            0,
            0});
            this.nudOffset.Name = "nudOffset";
            this.nudOffset.Size = new System.Drawing.Size(75, 20);
            this.nudOffset.TabIndex = 11;
            this.nudOffset.ValueChanged += new System.EventHandler(this.numericUpDown1_ValueChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(299, 125);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(41, 13);
            this.label5.TabIndex = 12;
            this.label5.Text = "Offset :";
            // 
            // picPointO
            // 
            this.picPointO.BackColor = System.Drawing.Color.Red;
            this.picPointO.Location = new System.Drawing.Point(9, 577);
            this.picPointO.Margin = new System.Windows.Forms.Padding(0);
            this.picPointO.Name = "picPointO";
            this.picPointO.Size = new System.Drawing.Size(18, 18);
            this.picPointO.TabIndex = 3;
            // 
            // picPointI
            // 
            this.picPointI.BackColor = System.Drawing.Color.Red;
            this.picPointI.Location = new System.Drawing.Point(945, 577);
            this.picPointI.Margin = new System.Windows.Forms.Padding(0);
            this.picPointI.Name = "picPointI";
            this.picPointI.Size = new System.Drawing.Size(18, 18);
            this.picPointI.TabIndex = 3;
            // 
            // picPointITemp
            // 
            this.picPointITemp.BackColor = System.Drawing.Color.Yellow;
            this.picPointITemp.Location = new System.Drawing.Point(118, 577);
            this.picPointITemp.Margin = new System.Windows.Forms.Padding(0);
            this.picPointITemp.Name = "picPointITemp";
            this.picPointITemp.Size = new System.Drawing.Size(18, 18);
            this.picPointITemp.TabIndex = 3;
            // 
            // FrmWizard
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Black;
            this.ClientSize = new System.Drawing.Size(972, 604);
            this.ControlBox = false;
            this.Controls.Add(this.picPointITemp);
            this.Controls.Add(this.picPointI);
            this.Controls.Add(this.picPointO);
            this.Controls.Add(this.picPointJ);
            this.Controls.Add(this.panel1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "FrmWizard";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Quick setup";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.FrmWizard_FormClosing);
            this.Load += new System.EventHandler(this.frmWizard_Load);
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.picDevice2)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.picDevice1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.nudOffset)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button btnDone;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label lblO;
        private System.Windows.Forms.Label lblI;
        private System.Windows.Forms.Label lblJ;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label lblMousePos;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Panel picPointJ;
        private System.Windows.Forms.PictureBox picDevice2;
        private System.Windows.Forms.PictureBox picDevice1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button btnPrevious;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.Label lblInfo;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label lblO2;
        private System.Windows.Forms.Label lblJ2;
        private System.Windows.Forms.Label lblI2;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.NumericUpDown nudOffset;
        private System.Windows.Forms.Panel picPointO;
        private System.Windows.Forms.Panel picPointI;
        private System.Windows.Forms.Panel picPointITemp;
    }
}