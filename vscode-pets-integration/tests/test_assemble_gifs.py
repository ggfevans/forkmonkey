"""
Unit tests for assemble_gifs.py - Fork Monkey GIF Assembly Script

Tests cover:
- Image processing functions (transparency removal, frame processing)
- GIF creation logic
- File I/O operations
- Error handling and edge cases
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open, call
from pathlib import Path
import os
import sys

# Add the script directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "experiment1" / "scripts" / "sprite-generation"))

# Import the module under test
import assemble_gifs


class TestRemoveAllSemitransparency:
    """Test the remove_all_semitransparency function"""
    
    @patch('assemble_gifs.Image')
    def test_convert_to_rgba_if_needed(self, mock_image_class):
        """Test that non-RGBA images are converted to RGBA"""
        mock_img = Mock()
        mock_img.mode = 'RGB'
        mock_rgba_img = Mock()
        mock_rgba_img.mode = 'RGBA'
        mock_rgba_img.size = (10, 10)
        mock_img.convert.return_value = mock_rgba_img
        
        # Mock the pixels
        mock_rgba_img.load.return_value = {(x, y): (100, 100, 100, 128) for x in range(10) for y in range(10)}
        
        result = assemble_gifs.remove_all_semitransparency(mock_img, threshold=200)
        
        mock_img.convert.assert_called_once_with('RGBA')
        assert result == mock_rgba_img
    
    def test_pixels_above_threshold_become_opaque(self):
        """Test that pixels with alpha > threshold become fully opaque"""
        from PIL import Image
        
        # Create a simple test image with semi-transparent pixels
        img = Image.new('RGBA', (2, 2), (100, 100, 100, 220))
        
        result = assemble_gifs.remove_all_semitransparency(img, threshold=200)
        
        pixels = result.load()
        # All pixels should be fully opaque (alpha=255)
        for x in range(2):
            for y in range(2):
                assert pixels[x, y][3] == 255, f"Pixel at ({x}, {y}) should be fully opaque"
    
    def test_pixels_below_threshold_become_transparent(self):
        """Test that pixels with alpha <= threshold become fully transparent"""
        from PIL import Image
        
        # Create a test image with low alpha values
        img = Image.new('RGBA', (2, 2), (100, 100, 100, 100))
        
        result = assemble_gifs.remove_all_semitransparency(img, threshold=200)
        
        pixels = result.load()
        # All pixels should be fully transparent (alpha=0)
        for x in range(2):
            for y in range(2):
                assert pixels[x, y] == (0, 0, 0, 0), f"Pixel at ({x}, {y}) should be fully transparent"
    
    def test_threshold_boundary_conditions(self):
        """Test pixels exactly at the threshold"""
        from PIL import Image
        
        threshold = 200
        
        # Test pixel exactly at threshold (should become transparent)
        img_at_threshold = Image.new('RGBA', (1, 1), (100, 100, 100, threshold))
        result = assemble_gifs.remove_all_semitransparency(img_at_threshold, threshold=threshold)
        pixels = result.load()
        assert pixels[0, 0][3] == 0, "Pixel at threshold should be transparent"
        
        # Test pixel just above threshold (should become opaque)
        img_above = Image.new('RGBA', (1, 1), (100, 100, 100, threshold + 1))
        result = assemble_gifs.remove_all_semitransparency(img_above, threshold=threshold)
        pixels = result.load()
        assert pixels[0, 0][3] == 255, "Pixel above threshold should be opaque"


class TestProcessFrame:
    """Test the process_frame function"""
    
    @patch('assemble_gifs.Image')
    def test_opens_and_converts_image(self, mock_image_class):
        """Test that frame is opened and converted to RGBA"""
        mock_img = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_img
        mock_img.mode = 'RGBA'
        mock_img.size = (100, 100)
        mock_img.width = 100
        mock_img.height = 100
        mock_img.getbbox.return_value = (10, 10, 90, 90)
        mock_img.crop.return_value = mock_img
        
        # Mock load() to return a dict-like object
        mock_pixels = {}
        for x in range(100):
            for y in range(100):
                mock_pixels[(x, y)] = (100, 100, 100, 255)
        mock_img.load.return_value = mock_pixels
        
        # Mock Image.new for final canvas
        mock_final = Mock()
        mock_final.width = 111
        mock_final.height = 101
        mock_image_class.new.return_value = mock_final
        
        with patch('assemble_gifs.remove_all_semitransparency', return_value=mock_img):
            assemble_gifs.process_frame("/fake/path.png", (111, 101))
        
        mock_image_class.open.assert_called_once_with("/fake/path.png")
    
    @patch('assemble_gifs.Image')
    def test_crops_to_content_bbox(self, mock_image_class):
        """Test that image is cropped to bounding box"""
        mock_img = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_img
        mock_img.mode = 'RGBA'
        mock_img.size = (100, 100)
        mock_img.width = 80
        mock_img.height = 80
        bbox = (10, 10, 90, 90)
        mock_img.getbbox.return_value = bbox
        mock_img.crop.return_value = mock_img
        
        mock_pixels = {}
        for x in range(80):
            for y in range(80):
                mock_pixels[(x, y)] = (100, 100, 100, 255)
        mock_img.load.return_value = mock_pixels
        
        mock_final = Mock()
        mock_image_class.new.return_value = mock_final
        
        with patch('assemble_gifs.remove_all_semitransparency', return_value=mock_img):
            assemble_gifs.process_frame("/fake/path.png", (111, 101))
        
        mock_img.crop.assert_called_once_with(bbox)
    
    @patch('assemble_gifs.Image')
    def test_centers_image_on_canvas(self, mock_image_class):
        """Test that processed image is centered on target canvas"""
        mock_img = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_img
        mock_img.mode = 'RGBA'
        mock_img.size = (50, 50)
        mock_img.width = 50
        mock_img.height = 50
        mock_img.getbbox.return_value = (0, 0, 50, 50)
        mock_img.crop.return_value = mock_img
        
        mock_pixels = {}
        for x in range(50):
            for y in range(50):
                mock_pixels[(x, y)] = (100, 100, 100, 255)
        mock_img.load.return_value = mock_pixels
        
        mock_final = Mock()
        mock_image_class.new.return_value = mock_final
        
        with patch('assemble_gifs.remove_all_semitransparency', return_value=mock_img):
            assemble_gifs.process_frame("/fake/path.png", (111, 101))
        
        # Image should be centered: (111-50)//2 = 30, (101-50)//2 = 25
        mock_final.paste.assert_called_once_with(mock_img, (30, 25), mock_img)
    
    @patch('assemble_gifs.Image')
    def test_removes_semitransparency_multiple_times(self, mock_image_class):
        """Test that semitransparency removal is called multiple times"""
        mock_img = Mock()
        mock_image_class.open.return_value.convert.return_value = mock_img
        mock_img.mode = 'RGBA'
        mock_img.size = (50, 50)
        mock_img.width = 50
        mock_img.height = 50
        mock_img.getbbox.return_value = (0, 0, 50, 50)
        mock_img.crop.return_value = mock_img
        
        mock_pixels = {}
        for x in range(50):
            for y in range(50):
                mock_pixels[(x, y)] = (100, 100, 100, 255)
        mock_img.load.return_value = mock_pixels
        
        mock_final = Mock()
        mock_image_class.new.return_value = mock_final
        
        with patch('assemble_gifs.remove_all_semitransparency', return_value=mock_img) as mock_remove:
            assemble_gifs.process_frame("/fake/path.png", (111, 101))
        
        # Should be called 3 times: after load, after resize, and final pass
        assert mock_remove.call_count == 3


class TestCreateGif:
    """Test the create_gif function"""
    
    @patch('assemble_gifs.os.path.exists')
    @patch('assemble_gifs.os.path.join')
    def test_returns_false_when_no_frames_found(self, mock_join, mock_exists):
        """Test that function returns False when no frames are found"""
        mock_exists.return_value = False
        mock_join.return_value = "/fake/path/frame_01.png"
        
        result = assemble_gifs.create_gif("test_anim", 4, "/fake/output.gif")
        
        assert result is False
    
    @patch('assemble_gifs.os.path.getsize')
    @patch('assemble_gifs.os.path.exists')
    @patch('assemble_gifs.os.path.join')
    @patch('assemble_gifs.process_frame')
    def test_processes_all_frames(self, mock_process, mock_join, mock_exists, mock_getsize):
        """Test that all available frames are processed"""
        mock_exists.return_value = True
        mock_join.side_effect = lambda d, f: f"/fake/{f}"
        mock_getsize.return_value = 1024
        
        mock_frame = Mock()
        mock_frame.save = Mock()
        mock_process.return_value = mock_frame
        
        result = assemble_gifs.create_gif("test_anim", 4, "/fake/output.gif")
        
        # Should call process_frame 4 times (frame_count)
        assert mock_process.call_count == 4
        assert result is True
    
    @patch('assemble_gifs.os.path.getsize')
    @patch('assemble_gifs.os.path.exists')
    @patch('assemble_gifs.os.path.join')
    @patch('assemble_gifs.process_frame')
    def test_saves_gif_with_correct_parameters(self, mock_process, mock_join, mock_exists, mock_getsize):
        """Test that GIF is saved with correct parameters"""
        mock_exists.return_value = True
        mock_join.side_effect = lambda d, f: f"/fake/{f}"
        mock_getsize.return_value = 1024
        
        mock_frames = [Mock() for _ in range(4)]
        mock_process.side_effect = mock_frames
        
        assemble_gifs.create_gif("test_anim", 4, "/fake/output.gif")
        
        # First frame should be used to save the GIF
        mock_frames[0].save.assert_called_once()
        call_kwargs = mock_frames[0].save.call_args[1]
        
        assert call_kwargs['save_all'] is True
        assert call_kwargs['duration'] == 250
        assert call_kwargs['loop'] == 0
        assert call_kwargs['disposal'] == 2
        assert call_kwargs['optimize'] is True


class TestMain:
    """Test the main function"""
    
    @patch('assemble_gifs.os.makedirs')
    @patch('assemble_gifs.create_gif')
    @patch('assemble_gifs.glob.glob')
    @patch('assemble_gifs.os.path.getsize')
    @patch('assemble_gifs.os.path.join')
    def test_creates_output_directory(self, mock_join, mock_getsize, mock_glob, mock_create_gif, mock_makedirs):
        """Test that output directory is created"""
        mock_create_gif.return_value = True
        mock_glob.return_value = []
        mock_getsize.return_value = 1024
        mock_join.return_value = "/fake/output.gif"
        
        assemble_gifs.main()
        
        mock_makedirs.assert_called_once_with(assemble_gifs.GIFS_DIR, exist_ok=True)
    
    @patch('assemble_gifs.os.makedirs')
    @patch('assemble_gifs.create_gif')
    @patch('assemble_gifs.glob.glob')
    @patch('assemble_gifs.os.path.getsize')
    @patch('assemble_gifs.os.path.join')
    def test_creates_all_animations(self, mock_join, mock_getsize, mock_glob, mock_create_gif, mock_makedirs):
        """Test that all defined animations are created"""
        mock_create_gif.return_value = True
        mock_glob.return_value = []
        mock_getsize.return_value = 1024
        mock_join.return_value = "/fake/output.gif"
        
        assemble_gifs.main()
        
        # Should call create_gif for each animation
        assert mock_create_gif.call_count == len(assemble_gifs.ANIMATIONS)
    
    @patch('assemble_gifs.os.makedirs')
    @patch('assemble_gifs.create_gif')
    @patch('assemble_gifs.glob.glob')
    @patch('assemble_gifs.os.path.getsize')
    @patch('assemble_gifs.os.path.join')
    def test_handles_partial_failures(self, mock_join, mock_getsize, mock_glob, mock_create_gif, mock_makedirs):
        """Test that main continues even if some GIFs fail"""
        # Make some animations succeed and some fail
        mock_create_gif.side_effect = [True, False, True, True, False]
        mock_glob.return_value = []
        mock_getsize.return_value = 1024
        mock_join.return_value = "/fake/output.gif"
        
        # Should not raise an exception
        assemble_gifs.main()
        
        assert mock_create_gif.call_count == len(assemble_gifs.ANIMATIONS)


class TestConstants:
    """Test that constants are properly defined"""
    
    def test_target_size_is_valid(self):
        """Test that TARGET_SIZE is a valid tuple"""
        assert isinstance(assemble_gifs.TARGET_SIZE, tuple)
        assert len(assemble_gifs.TARGET_SIZE) == 2
        assert all(isinstance(x, int) and x > 0 for x in assemble_gifs.TARGET_SIZE)
    
    def test_animations_dict_is_valid(self):
        """Test that ANIMATIONS dictionary is properly structured"""
        assert isinstance(assemble_gifs.ANIMATIONS, dict)
        assert len(assemble_gifs.ANIMATIONS) > 0
        
        for name, frame_count in assemble_gifs.ANIMATIONS.items():
            assert isinstance(name, str)
            assert isinstance(frame_count, int)
            assert frame_count > 0
    
    def test_frame_duration_is_positive(self):
        """Test that FRAME_DURATION is positive"""
        assert isinstance(assemble_gifs.FRAME_DURATION, int)
        assert assemble_gifs.FRAME_DURATION > 0
    
    def test_fps_matches_duration(self):
        """Test that FPS and FRAME_DURATION are consistent"""
        # FPS = 4 should result in 250ms per frame (1000ms / 4 = 250ms)
        expected_duration = 1000 // assemble_gifs.FPS
        assert assemble_gifs.FRAME_DURATION == expected_duration


class TestIntegrationScenarios:
    """Integration-style tests for end-to-end scenarios"""
    
    def test_process_frame_with_real_image(self):
        """Test processing a real image (integration test)"""
        from PIL import Image
        import tempfile
        
        # Create a temporary test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            test_img = Image.new('RGBA', (100, 100), (255, 0, 0, 200))
            test_img.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            result = assemble_gifs.process_frame(tmp_path, (111, 101))
            
            assert result is not None
            assert result.size == (111, 101)
            assert result.mode == 'RGBA'
        finally:
            os.unlink(tmp_path)
    
    def test_transparency_removal_on_real_image(self):
        """Test transparency removal on a real image"""
        from PIL import Image
        
        # Create an image with mixed transparency
        img = Image.new('RGBA', (10, 10))
        pixels = img.load()
        
        # Set different alpha values
        for x in range(10):
            for y in range(10):
                if x < 5:
                    pixels[x, y] = (100, 100, 100, 250)  # Should become opaque
                else:
                    pixels[x, y] = (100, 100, 100, 50)   # Should become transparent
        
        result = assemble_gifs.remove_all_semitransparency(img, threshold=200)
        result_pixels = result.load()
        
        # Check that transparency was properly binarized
        for x in range(5):
            for y in range(10):
                assert result_pixels[x, y][3] == 255  # Opaque
        
        for x in range(5, 10):
            for y in range(10):
                assert result_pixels[x, y][3] == 0  # Transparent


# Pytest configuration for this test module
@pytest.fixture(autouse=True)
def reset_module_state():
    """Reset any module-level state between tests"""
    yield
    # Cleanup code here if needed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])