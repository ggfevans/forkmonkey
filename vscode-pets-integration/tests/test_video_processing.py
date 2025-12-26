"""
Unit tests for experiment2 video processing scripts

Tests cover all video-to-gif conversion scripts:
- video_to_gif.py (walking animation)
- create_idle_gif.py
- create_run_gif.py
- create_swipe_gif.py
- create_with_ball_gif.py

Tests include:
- Frame extraction from video using ffmpeg
- White background removal
- Image processing and resizing
- GIF creation with proper settings
- File I/O operations
- Error handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import subprocess
import sys

# Add the script directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "experiment2" / "scripts"))


class TestExtractFramesFromVideo:
    """Test frame extraction functionality (common across all scripts)"""
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('glob.glob')
    def test_creates_output_directory(self, mock_glob, mock_makedirs, mock_run):
        """Test that output directory is created"""
        mock_run.return_value = Mock(returncode=0)
        mock_glob.return_value = ['/tmp/frame_001.png']
        
        # Import any of the scripts to test (they share this function)
        import video_to_gif
        
        video_to_gif.extract_frames_from_video('/fake/video.mp4', '/tmp/output', fps=4)
        
        mock_makedirs.assert_called_once_with('/tmp/output', exist_ok=True)
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('glob.glob')
    def test_calls_ffmpeg_with_correct_arguments(self, mock_glob, mock_makedirs, mock_run):
        """Test that ffmpeg is called with correct parameters"""
        mock_run.return_value = Mock(returncode=0)
        mock_glob.return_value = ['/tmp/frame_001.png']
        
        import video_to_gif
        
        video_to_gif.extract_frames_from_video('/fake/video.mp4', '/tmp/output', fps=4)
        
        # Check ffmpeg command
        call_args = mock_run.call_args[0][0]
        assert 'ffmpeg' in call_args
        assert '-i' in call_args
        assert '/fake/video.mp4' in call_args
        assert 'fps=4' in ' '.join(call_args)
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('glob.glob')
    def test_returns_sorted_frame_list(self, mock_glob, mock_makedirs, mock_run):
        """Test that extracted frames are returned as sorted list"""
        mock_run.return_value = Mock(returncode=0)
        mock_glob.return_value = [
            '/tmp/frame_003.png',
            '/tmp/frame_001.png', 
            '/tmp/frame_002.png'
        ]
        
        import video_to_gif
        
        result = video_to_gif.extract_frames_from_video('/fake/video.mp4', '/tmp/output', fps=4)
        
        # Result should be sorted
        assert result == sorted(mock_glob.return_value)
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('glob.glob')
    def test_returns_false_on_ffmpeg_error(self, mock_glob, mock_makedirs, mock_run):
        """Test that False is returned when ffmpeg fails"""
        mock_run.return_value = Mock(returncode=1, stderr='ffmpeg error')
        
        import video_to_gif
        
        result = video_to_gif.extract_frames_from_video('/fake/video.mp4', '/tmp/output', fps=4)
        
        assert result is False
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    @patch('glob.glob')
    def test_uses_custom_fps(self, mock_glob, mock_makedirs, mock_run):
        """Test that custom FPS parameter is used"""
        mock_run.return_value = Mock(returncode=0)
        mock_glob.return_value = ['/tmp/frame_001.png']
        
        import video_to_gif
        
        video_to_gif.extract_frames_from_video('/fake/video.mp4', '/tmp/output', fps=8)
        
        call_args = mock_run.call_args[0][0]
        assert 'fps=8' in ' '.join(call_args)


class TestRemoveWhiteBackground:
    """Test white background removal functionality"""
    
    def test_removes_white_pixels(self):
        """Test that white pixels are made transparent"""
        from PIL import Image
        import video_to_gif
        
        # Create image with white background
        img = Image.new('RGBA', (10, 10), (255, 255, 255, 255))
        
        result = video_to_gif.remove_white_background(img, threshold=240)
        
        pixels = result.load()
        # All pixels should be transparent
        for x in range(10):
            for y in range(10):
                assert pixels[x, y][3] == 0, f"Pixel at ({x}, {y}) should be transparent"
    
    def test_preserves_colored_pixels(self):
        """Test that non-white pixels are preserved as opaque"""
        from PIL import Image
        import video_to_gif
        
        # Create image with colored pixels
        img = Image.new('RGBA', (10, 10), (100, 100, 100, 255))
        
        result = video_to_gif.remove_white_background(img, threshold=240)
        
        pixels = result.load()
        # All pixels should be opaque
        for x in range(10):
            for y in range(10):
                assert pixels[x, y][3] == 255, f"Pixel at ({x}, {y}) should be opaque"
    
    def test_threshold_boundary_handling(self):
        """Test handling of pixels at threshold boundary"""
        from PIL import Image
        import video_to_gif
        
        threshold = 240
        
        # Create image with pixels exactly at threshold
        img = Image.new('RGBA', (5, 5), (threshold, threshold, threshold, 255))
        result = video_to_gif.remove_white_background(img, threshold=threshold)
        pixels = result.load()
        
        # Pixels at threshold should be transparent
        assert pixels[0, 0][3] == 0
        
        # Create image with pixels just below threshold
        img2 = Image.new('RGBA', (5, 5), (threshold-1, threshold-1, threshold-1, 255))
        result2 = video_to_gif.remove_white_background(img2, threshold=threshold)
        pixels2 = result2.load()
        
        # Pixels below threshold should be opaque
        assert pixels2[0, 0][3] == 255
    
    def test_converts_non_rgba_to_rgba(self):
        """Test that non-RGBA images are converted"""
        from PIL import Image
        import video_to_gif
        
        # Create RGB image
        img = Image.new('RGB', (5, 5), (100, 100, 100))
        
        result = video_to_gif.remove_white_background(img, threshold=240)
        
        assert result.mode == 'RGBA'


class TestProcessFrame:
    """Test frame processing functionality"""
    
    @patch('video_to_gif.Image')
    def test_opens_and_processes_image(self, mock_image_class):
        """Test that image is opened and processed"""
        import video_to_gif
        
        mock_img = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_img
        mock_img.mode = 'RGBA'
        mock_img.size = (100, 100)
        mock_img.width = 50
        mock_img.height = 50
        mock_img.getbbox.return_value = (10, 10, 60, 60)
        
        mock_cropped = Mock()
        mock_cropped.width = 50
        mock_cropped.height = 50
        mock_img.crop.return_value = mock_cropped
        
        mock_pixels = {}
        for x in range(50):
            for y in range(50):
                mock_pixels[(x, y)] = (100, 100, 100, 255)
        mock_cropped.load.return_value = mock_pixels
        
        mock_final = Mock()
        mock_image_class.new.return_value = mock_final
        
        with patch('video_to_gif.remove_white_background', return_value=mock_img):
            video_to_gif.process_frame('/fake/frame.png', (111, 101))
        
        mock_image_class.open.assert_called_once_with('/fake/frame.png')
    
    @patch('video_to_gif.Image')
    def test_crops_to_bounding_box(self, mock_image_class):
        """Test that image is cropped to content bounding box"""
        import video_to_gif
        
        mock_img = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_img
        mock_img.mode = 'RGBA'
        mock_img.size = (100, 100)
        mock_img.width = 50
        mock_img.height = 50
        bbox = (10, 10, 60, 60)
        mock_img.getbbox.return_value = bbox
        
        mock_cropped = Mock()
        mock_cropped.width = 50
        mock_cropped.height = 50
        mock_img.crop.return_value = mock_cropped
        
        mock_pixels = {}
        for x in range(50):
            for y in range(50):
                mock_pixels[(x, y)] = (100, 100, 100, 255)
        mock_cropped.load.return_value = mock_pixels
        
        mock_final = Mock()
        mock_image_class.new.return_value = mock_final
        
        with patch('video_to_gif.remove_white_background', return_value=mock_img):
            video_to_gif.process_frame('/fake/frame.png', (111, 101))
        
        mock_img.crop.assert_called_once_with(bbox)
    
    @patch('video_to_gif.Image')
    def test_removes_semi_transparency(self, mock_image_class):
        """Test that semi-transparent pixels are handled"""
        from PIL import Image
        import video_to_gif
        
        # Create a real image with semi-transparent pixels
        img = Image.new('RGBA', (10, 10))
        pixels = img.load()
        
        # Set pixels with varying alpha values
        for x in range(10):
            for y in range(10):
                if x < 5:
                    pixels[x, y] = (100, 100, 100, 150)  # Semi-transparent
                else:
                    pixels[x, y] = (100, 100, 100, 50)   # More transparent
        
        with patch('video_to_gif.Image.open') as mock_open:
            mock_open.return_value.convert.return_value = img
            
            result = video_to_gif.process_frame('/fake/frame.png', (111, 101))
        
        # Result should have binary transparency
        assert result.mode == 'RGBA'
    
    @patch('video_to_gif.Image')
    def test_centers_on_target_canvas(self, mock_image_class):
        """Test that processed image is centered on target canvas"""
        import video_to_gif
        
        mock_img = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_img
        mock_img.mode = 'RGBA'
        mock_img.size = (50, 50)
        mock_img.width = 50
        mock_img.height = 50
        mock_img.getbbox.return_value = (0, 0, 50, 50)
        
        mock_cropped = Mock()
        mock_cropped.width = 50
        mock_cropped.height = 50
        mock_img.crop.return_value = mock_cropped
        
        mock_pixels = {}
        for x in range(50):
            for y in range(50):
                mock_pixels[(x, y)] = (100, 100, 100, 255)
        mock_cropped.load.return_value = mock_pixels
        
        mock_final = Mock()
        mock_image_class.new.return_value = mock_final
        
        with patch('video_to_gif.remove_white_background', return_value=mock_img):
            video_to_gif.process_frame('/fake/frame.png', (111, 101))
        
        # Image should be centered: (111-50)//2 = 30, (101-50)//2 = 25
        expected_pos = (30, 25)
        mock_final.paste.assert_called_once()
        actual_pos = mock_final.paste.call_args[0][1]
        assert actual_pos == expected_pos


class TestCreateWalkingCycle:
    """Test walking cycle GIF creation (video_to_gif.py)"""
    
    @patch('video_to_gif.os.path.getsize')
    @patch('video_to_gif.process_frame')
    def test_selects_evenly_spaced_frames(self, mock_process, mock_getsize):
        """Test that frames are selected evenly across available frames"""
        import video_to_gif
        
        mock_getsize.return_value = 1024
        mock_frame = Mock()
        mock_frame.save = Mock()
        mock_process.return_value = mock_frame
        
        # Provide 24 frames, request 6-frame cycle
        frame_files = [f'/tmp/frame_{i:03d}.png' for i in range(1, 25)]
        
        video_to_gif.create_walking_cycle(frame_files, '/tmp/output.gif', cycle_length=6)
        
        # Should process 6 frames
        assert mock_process.call_count == 6
    
    @patch('video_to_gif.os.path.getsize')
    @patch('video_to_gif.process_frame')
    def test_saves_gif_with_correct_parameters(self, mock_process, mock_getsize):
        """Test that GIF is saved with correct parameters"""
        import video_to_gif
        
        mock_getsize.return_value = 1024
        mock_frames = [Mock() for _ in range(6)]
        mock_process.side_effect = mock_frames
        
        frame_files = [f'/tmp/frame_{i:03d}.png' for i in range(1, 7)]
        
        video_to_gif.create_walking_cycle(frame_files, '/tmp/output.gif', cycle_length=6)
        
        # First frame should save the GIF
        mock_frames[0].save.assert_called_once()
        call_kwargs = mock_frames[0].save.call_args[1]
        
        assert call_kwargs['save_all'] is True
        assert call_kwargs['duration'] == 250
        assert call_kwargs['loop'] == 0
        assert call_kwargs['disposal'] == 2


class TestCreateIdleCycle:
    """Test idle cycle GIF creation"""
    
    @patch('create_idle_gif.os.path.getsize')
    @patch('create_idle_gif.process_frame')
    def test_creates_4_frame_idle_cycle(self, mock_process, mock_getsize):
        """Test that idle cycle uses 4 frames"""
        import create_idle_gif
        
        mock_getsize.return_value = 1024
        mock_frame = Mock()
        mock_frame.save = Mock()
        mock_process.return_value = mock_frame
        
        frame_files = [f'/tmp/idle_frame_{i:03d}.png' for i in range(1, 25)]
        
        create_idle_gif.create_idle_cycle(frame_files, '/tmp/output.gif', cycle_length=4)
        
        # Should process exactly 4 frames
        assert mock_process.call_count == 4


class TestCreateRunningCycle:
    """Test running cycle GIF creation"""
    
    @patch('create_run_gif.os.path.getsize')
    @patch('create_run_gif.process_frame')
    def test_creates_8_frame_running_cycle(self, mock_process, mock_getsize):
        """Test that running cycle uses 8 frames for dynamic motion"""
        import create_run_gif
        
        mock_getsize.return_value = 1024
        mock_frame = Mock()
        mock_frame.save = Mock()
        mock_process.return_value = mock_frame
        
        frame_files = [f'/tmp/run_frame_{i:03d}.png' for i in range(1, 25)]
        
        create_run_gif.create_running_cycle(frame_files, '/tmp/output.gif', cycle_length=8)
        
        # Should process exactly 8 frames
        assert mock_process.call_count == 8


class TestCreateSwipeCycle:
    """Test swipe/eating cycle GIF creation"""
    
    @patch('create_swipe_gif.os.path.getsize')
    @patch('create_swipe_gif.process_frame')
    def test_creates_5_frame_swipe_cycle(self, mock_process, mock_getsize):
        """Test that swipe cycle uses 5 frames"""
        import create_swipe_gif
        
        mock_getsize.return_value = 1024
        mock_frame = Mock()
        mock_frame.save = Mock()
        mock_process.return_value = mock_frame
        
        frame_files = [f'/tmp/swipe_frame_{i:03d}.png' for i in range(1, 25)]
        
        create_swipe_gif.create_swipe_cycle(frame_files, '/tmp/output.gif', cycle_length=5)
        
        # Should process exactly 5 frames
        assert mock_process.call_count == 5


class TestCreateWithBallCycle:
    """Test with_ball cycle GIF creation"""
    
    @patch('create_with_ball_gif.os.path.getsize')
    @patch('create_with_ball_gif.process_frame')
    def test_creates_4_frame_with_ball_cycle(self, mock_process, mock_getsize):
        """Test that with_ball cycle uses 4 frames"""
        import create_with_ball_gif
        
        mock_getsize.return_value = 1024
        mock_frame = Mock()
        mock_frame.save = Mock()
        mock_process.return_value = mock_frame
        
        frame_files = [f'/tmp/ball_frame_{i:03d}.png' for i in range(1, 25)]
        
        create_with_ball_gif.create_with_ball_cycle(frame_files, '/tmp/output.gif', cycle_length=4)
        
        # Should process exactly 4 frames
        assert mock_process.call_count == 4


class TestMainFunctions:
    """Test main functions of each script"""
    
    @patch('video_to_gif.create_walking_cycle')
    @patch('video_to_gif.extract_frames_from_video')
    @patch('video_to_gif.os.makedirs')
    def test_video_to_gif_main(self, mock_makedirs, mock_extract, mock_create):
        """Test video_to_gif main function"""
        import video_to_gif
        
        mock_extract.return_value = ['/tmp/frame_001.png', '/tmp/frame_002.png']
        mock_create.return_value = True
        
        video_to_gif.main()
        
        mock_extract.assert_called_once()
        mock_create.assert_called_once()
    
    @patch('create_idle_gif.create_idle_cycle')
    @patch('create_idle_gif.extract_frames_from_video')
    @patch('create_idle_gif.os.makedirs')
    def test_create_idle_gif_main(self, mock_makedirs, mock_extract, mock_create):
        """Test create_idle_gif main function"""
        import create_idle_gif
        
        mock_extract.return_value = ['/tmp/idle_frame_001.png']
        mock_create.return_value = True
        
        create_idle_gif.main()
        
        mock_extract.assert_called_once()
        mock_create.assert_called_once()
    
    @patch('create_run_gif.create_running_cycle')
    @patch('create_run_gif.extract_frames_from_video')
    @patch('create_run_gif.os.makedirs')
    def test_create_run_gif_main(self, mock_makedirs, mock_extract, mock_create):
        """Test create_run_gif main function"""
        import create_run_gif
        
        mock_extract.return_value = ['/tmp/run_frame_001.png']
        mock_create.return_value = True
        
        create_run_gif.main()
        
        mock_extract.assert_called_once()
        mock_create.assert_called_once()


class TestConstants:
    """Test that constants are properly defined across all scripts"""
    
    def test_target_size_is_consistent(self):
        """Test that TARGET_SIZE is consistent across all scripts"""
        import video_to_gif
        import create_idle_gif
        import create_run_gif
        import create_swipe_gif
        import create_with_ball_gif
        
        expected_size = (111, 101)
        
        assert video_to_gif.TARGET_SIZE == expected_size
        assert create_idle_gif.TARGET_SIZE == expected_size
        assert create_run_gif.TARGET_SIZE == expected_size
        assert create_swipe_gif.TARGET_SIZE == expected_size
        assert create_with_ball_gif.TARGET_SIZE == expected_size
    
    def test_frame_duration_is_consistent(self):
        """Test that FRAME_DURATION is consistent across all scripts"""
        import video_to_gif
        import create_idle_gif
        import create_run_gif
        
        expected_duration = 250
        
        assert video_to_gif.FRAME_DURATION == expected_duration
        assert create_idle_gif.FRAME_DURATION == expected_duration
        assert create_run_gif.FRAME_DURATION == expected_duration


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @patch('video_to_gif.extract_frames_from_video')
    @patch('video_to_gif.os.makedirs')
    def test_handles_extraction_failure(self, mock_makedirs, mock_extract):
        """Test handling of frame extraction failure"""
        import video_to_gif
        
        mock_extract.return_value = False
        
        # Should not raise exception
        video_to_gif.main()
    
    @patch('subprocess.run')
    @patch('os.makedirs')
    def test_handles_ffmpeg_not_found(self, mock_makedirs, mock_run):
        """Test handling when ffmpeg is not available"""
        import video_to_gif
        
        mock_run.side_effect = FileNotFoundError("ffmpeg not found")
        
        with pytest.raises(FileNotFoundError):
            video_to_gif.extract_frames_from_video('/fake/video.mp4', '/tmp/output', fps=4)


class TestIntegrationScenarios:
    """Integration-style tests"""
    
    def test_process_frame_with_real_image(self):
        """Test processing a real image"""
        from PIL import Image
        import tempfile
        import os
        import video_to_gif
        
        # Create a temporary test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            test_img = Image.new('RGBA', (100, 100), (255, 0, 0, 200))
            test_img.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            result = video_to_gif.process_frame(tmp_path, (111, 101))
            
            assert result is not None
            assert result.size == (111, 101)
            assert result.mode == 'RGBA'
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])