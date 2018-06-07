% camera_ctrl - provides basic control of QSI RS 6.1s CCD camera
%
% He Sun from Princeton HCIL - Sep. 4, 2015
% Updates from Christian Delacroix - 2018
%
% Brief useage:
%   Connect the camera:
%           camera.name = 'QSICamera.CCDCamera';
%           camera = Camera_ctrl(camera, 'connect');
%   Disconnect the camera:
%           camera = Camera_ctrl(camera, 'disconnect');
%   Initialization:
%           Camera_ctrl(camera, 'init', ccdtemp); % temperature: range -50 to
%           50
%   Stop fan and cooler:
%           Camera_ctrl(camera, 'finalize');
%   Disable the camera:
%           Camera_ctrl(camera, 'disable');
%   Open or close shutter;
%           camera = Camera_ctrl(camera, 'shutter', openflag); % openflag: 1 for open
%           0 for close
%   Set readout speed:
%           Camera_ctrl(camera, 'readoutspeed', readoutflag); % readoutflag: 1
%           for fast readout, 0 for high image quality
%   Exposure properties:
%           camera = Camera_ctrl(camera, 'exposureproperties', startPos, imgSize,...
%                       binPix); % the last three input arguments are
%                       all 2 dimension vectors, the default values are
%                       [0,0], [2758,2208], [1,1]
%   Set shutter priority:
%           Camera_ctrl(camera, 'shutterpriority', shutterflag); % shutterflag:
%           0 for mechanical, 1 for electrical
%   Take pictures:
%           img = Camera_ctrl(camera, 'exposure', expTime); % exposure time in seconds
%   Show camera realtime picture:
%           Camera_ctrl(camera, 'realtime'); % can be used during calibration

function output = Camera_ctrl(camera, cmd, varargin)

    n_argin = size(varargin,2);
    switch(lower(cmd))
        
        case 'connect'
            try 
                % get a handle of the camera
                if not(isfield(camera, 'handle'))
                    camera.handle = actxserver(char(camera.name));
                end
                % connect the camera
                if not(camera.handle.Connected)
                    camera.handle.Connected = 1;
                    disp(['Connecting ' class(camera.handle)])
                else
                    disp([class(camera.handle) ' is already connected.'])
                end
                % get camera default parameters
                camera.serialnum = camera.handle.SerialNumber;
                camera.defaultsizepixels = [camera.handle.NumX, camera.handle.NumY];
                camera.defaultstartpos = [0,0];
                camera.defaultbinpixels = [1,1];
                camera = Camera_ctrl(camera, 'shutter', 1); % open shutter
            catch ME
                switch ME.identifier
                    case 'MATLAB:COM:InvalidProgid'
                        fprintf ( 2, [camera.name +': wrong camera name!\n\n'] )
                        disp([camera.name +': wrong camera name.'])
                    case 'MATLAB:COM:E2147748395'
                        fprintf ( 2, 'Lost handle of camera, unplug USB manually!\n\n' )
                        camera = rmfield(camera, 'handle');
                    otherwise
                        rethrow(ME)
                end
            end
            output = camera;

        case 'disconnect'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            camera = Camera_ctrl(camera, 'shutter', 0); % close shutter
            Camera_ctrl(camera, 'finalize');
            Camera_ctrl(camera, 'disable');
            disp(['Disconnecting ' class(camera.handle)])
            camera = rmfield(camera, 'handle');
            output = camera;
            
        case 'init'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            assert(n_argin==1, 'Wrong number of input arguments');
            % set current camera as the main camera
            if not(camera.handle.IsMainCamera)
            	camera.handle.IsMaincamera = 1;
            end
            % turn on the camera fan
            if not(strcmp(camera.handle.FanMode, 'FanFull')) % if FanOff
                camera.handle.FanMode = 'FanFull';
            end
            % enable the CCD cooler
            if not(camera.handle.CoolerOn)
                camera.handle.CoolerOn = 1;
            end
            % set camera cooling temperature, and update ccdtemp attribute
            ccdtemp = cell2mat(varargin(1));
            if camera.handle.CanSetCCDTemperature
                camera.handle.SetCCDTemperature = ccdtemp;
            end
            camera.ccdtemp = camera.handle.SetCCDTemperature;
            % set camera gain to low gain
            if not(strcmp(camera.handle.CameraGain, 'CameraGainLow')) % if CameraGainHigh
                camera.handle.CameraGain = 'CameraGainLow';
            end
            % set camera shutter priority to electrical
            camera.handle.shutterpriority = 1; % 0 for mechanical, 1 for electrical
            output = camera;

        case 'shutter'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            assert(n_argin==1);
            openflag = cell2mat(varargin(1));
            if  openflag== 1;
                % Set the camera to manual shutter mode
                set(camera.handle, 'ManualShutterMode', 1);
                % Open the shutter as specified
                set(camera.handle, 'ManualShutterOpen', 1);
                camera.shutter = 1;
            else
                % Set the camera to manual shutter mode
                set(camera.handle, 'ManualShutterMode', 1);
                % Close the shutter as specified
                set(camera.handle, 'ManualShutterOpen', 0);
                % Set the camera to auto shutter mode
                set(camera.handle, 'ManualShutterMode', 0);
                camera.shutter = 0;
            end
            output = camera;
            
        case 'exposureproperties'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            assert(n_argin==3,'Wrong number of input arguments');
            startPos = cell2mat(varargin(1));
            imgSize = cell2mat(varargin(2));
            binPix = cell2mat(varargin(3));
            assert(length(startPos)==2, 'Wrong dimension of start position');
            assert(length(imgSize)==2, 'Wrong dimension of image size');
            assert(length(binPix)==2, 'Wrong dimension of binned pixels');
            %assert((startPos(1)+imgSize(1))*binPix(1)<=h.defaultsizepixels(1), 'x pixels exceeds chip range!');
            %assert((startPos(2)+imgSize(2))*binPix(2)<=h.defaultsizepixels(2), 'x pixels exceeds chip range!');
            camera.handle.StartX = startPos(1);
            camera.handle.StartY = startPos(2);
            camera.handle.NumX = imgSize(1);
            camera.handle.NumY = imgSize(2);
            camera.handle.BinX = binPix(1);
            camera.handle.BinY = binPix(2);
            % update camera attributes
            camera.startPos = [camera.handle.StartX, camera.handle.StartY];
            camera.imgSize = [camera.handle.NumX, camera.handle.NumY];
            camera.binPix = [camera.handle.BinX, camera.handle.BinY];
            output = camera;
            
        case 'avgimg'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            assert(n_argin==2, 'Wrong number of input arguments');
            camera.handle.readoutspeed = camera.fastReadout;
            expTime = cell2mat(varargin(1));
            numIm = cell2mat(varargin(2));
            img = int32(zeros(camera.imgSize(2), camera.imgSize(1)));
            for itr = 1:numIm
                img = img + Camera_ctrl(camera, 'exposure', expTime);
            end
            output = img / numIm;
            
        case 'exposure'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            assert(n_argin==1, 'Wrong number of input arguments');
            assert(camera.shutter==1||camera.shutter==0, 'The shutter status is incorrect');
            expTime = cell2mat(varargin(1));
            invoke(camera.handle, 'StartExposure', expTime, camera.shutter);
            % Wait for the exposure to complete
            done = get(camera.handle, 'ImageReady');
            while not(done)
                done = get(camera.handle, 'ImageReady');
            end
            output = get(camera.handle, 'ImageArray')';
            
        case 'realtime'
            f = figure(100);
            set(f, 'Name', 'Real Time Picture');
            %set(camera.handle, 'ShutterPriority', 1);
            while(ishandle(f))
                img = Camera_ctrl(camera, 'exposure', 0.0003);
                figure(100),imagesc(img), axis xy tight, colorbar;
                drawnow
            end
            output = 1;
            
        case 'readoutspeed'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            assert(n_argin==1,'Wrong number of input arguments');
            readoutflag = cell2mat(varargin(1));
            set(camera.handle, 'readoutspeed', readoutflag);
            output = 1;
        case 'shutterpriority'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            assert(n_argin==1,'Wrong number of input arguments');
            shutterflag = cell2mat(varargin(1));
            set(camera.handle, 'shutterpriority', shutterflag);
            output = 1;
        case 'finalize'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            % turn off the camera fan
            temp=get(camera.handle, 'FanMode');
            if strcmpi(temp,'FanOff') ~= 1
                set(camera.handle, 'FanMode', 'FanOff');
            end
            % disable the CCD cooler
            temp=get(camera.handle, 'CoolerOn');
            if temp ~= 0
                set(camera.handle, 'CoolerOn', 0);
            end
            Camera_ctrl(camera, 'shutter', 0);
            output = 1;
        case 'disable'
            assert(isfield(camera, 'handle'), 'Camera not connected.')
            % disconnect camera
            temp=get(camera.handle, 'Connected');
            if temp == 1
                set(camera.handle, 'Connected', 0);
            end
            output = 0;
            
        otherwise
            disp([ 'unknown command ' cmd ]);
            output = -1;
    end
end