"""
Unit tests for test_gemini.py - Gemini API Connection Test Script

Tests cover:
- API connection testing
- Image generation testing
- Error handling and validation
- Environment variable handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# Add the script directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "experiment1" / "scripts" / "sprite-generation"))

import test_gemini


class TestTestGeminiConnection:
    """Test the test_gemini_connection function"""
    
    def test_returns_false_when_api_key_missing(self):
        """Test that function returns False when API key is not set"""
        with patch.dict('os.environ', {}, clear=True):
            success, client = test_gemini.test_gemini_connection()
            
            assert success is False
            assert client is None
    
    def test_returns_api_key_preview(self):
        """Test that function displays API key preview (first 20 chars)"""
        test_key = "abcdefghijklmnopqrstuvwxyz123456"
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': test_key}):
            with patch('test_gemini.genai.Client') as mock_client_class:
                mock_client_class.return_value = Mock()
                
                success, client = test_gemini.test_gemini_connection()
                
                # Should successfully create client
                assert success is True
    
    @patch('test_gemini.genai.Client')
    def test_creates_client_successfully(self, mock_client_class):
        """Test successful client creation"""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            success, client = test_gemini.test_gemini_connection()
            
            assert success is True
            assert client == mock_client
            mock_client_class.assert_called_once_with(api_key='test_key')
    
    @patch('test_gemini.genai.Client')
    def test_handles_client_creation_exception(self, mock_client_class):
        """Test handling of exception during client creation"""
        mock_client_class.side_effect = Exception("Connection failed")
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            success, client = test_gemini.test_gemini_connection()
            
            assert success is False
            assert client is None


class TestTestImageGeneration:
    """Test the test_image_generation function"""
    
    @patch('test_gemini.PILImage')
    def test_generates_image_successfully(self, mock_pil_image):
        """Test successful image generation"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_part.text = None
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_img = Mock()
        mock_img.size = (1024, 1024)
        mock_img.mode = 'RGBA'
        mock_pil_image.open.return_value = mock_img
        
        with patch('os.path.exists', return_value=True):
            result = test_gemini.test_image_generation(mock_client)
        
        assert result is True
        mock_img.save.assert_called_once()
    
    def test_uses_correct_model(self):
        """Test that correct model is used for image generation"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        with patch('test_gemini.PILImage'):
            with patch('os.path.exists', return_value=True):
                test_gemini.test_image_generation(mock_client)
        
        call_args = mock_client.models.generate_content.call_args
        assert call_args[1]['model'] == "gemini-2.5-flash-image"
    
    def test_includes_image_config(self):
        """Test that image configuration is included"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        with patch('test_gemini.PILImage'):
            with patch('os.path.exists', return_value=True):
                test_gemini.test_image_generation(mock_client)
        
        call_args = mock_client.models.generate_content.call_args
        config = call_args[1]['config']
        assert config.response_modalities == ['IMAGE']
    
    def test_returns_false_when_no_image_in_response(self):
        """Test handling when no image is returned"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.parts = []
        mock_client.models.generate_content.return_value = mock_response
        
        result = test_gemini.test_image_generation(mock_client)
        
        assert result is False
    
    def test_handles_text_response_instead_of_image(self):
        """Test handling when API returns text instead of image"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data = None
        mock_part.text = "Text response instead of image"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        result = test_gemini.test_image_generation(mock_client)
        
        assert result is False
    
    def test_handles_api_exception(self):
        """Test handling of API exceptions"""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = Exception("API Error")
        
        result = test_gemini.test_image_generation(mock_client)
        
        assert result is False
    
    @patch('test_gemini.PILImage')
    def test_saves_to_correct_path(self, mock_pil_image):
        """Test that image is saved to the correct path"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_img = Mock()
        mock_img.size = (1024, 1024)
        mock_img.mode = 'RGBA'
        mock_pil_image.open.return_value = mock_img
        
        with patch('os.path.exists', return_value=True):
            test_gemini.test_image_generation(mock_client)
        
        save_path = mock_img.save.call_args[0][0]
        assert 'test_image.png' in save_path
    
    @patch('test_gemini.PILImage')
    def test_prompt_includes_key_requirements(self, mock_pil_image):
        """Test that prompt includes key requirements"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_img = Mock()
        mock_img.size = (1024, 1024)
        mock_img.mode = 'RGBA'
        mock_pil_image.open.return_value = mock_img
        
        with patch('os.path.exists', return_value=True):
            test_gemini.test_image_generation(mock_client)
        
        call_args = mock_client.models.generate_content.call_args
        prompt = call_args[1]['contents']
        
        assert 'pixel art' in prompt.lower()
        assert 'monkey' in prompt.lower()
        assert 'transparent background' in prompt.lower()
        assert '111x101' in prompt


class TestMain:
    """Test the main function"""
    
    @patch('test_gemini.test_image_generation')
    @patch('test_gemini.test_gemini_connection')
    def test_exits_when_connection_fails(self, mock_test_conn, mock_test_img):
        """Test that main exits when connection test fails"""
        mock_test_conn.return_value = (False, None)
        
        test_gemini.main()
        
        # Image generation should not be called if connection failed
        mock_test_img.assert_not_called()
    
    @patch('test_gemini.test_image_generation')
    @patch('test_gemini.test_gemini_connection')
    def test_runs_image_generation_after_connection(self, mock_test_conn, mock_test_img):
        """Test that image generation runs after successful connection"""
        mock_client = Mock()
        mock_test_conn.return_value = (True, mock_client)
        mock_test_img.return_value = True
        
        test_gemini.main()
        
        mock_test_img.assert_called_once_with(mock_client)
    
    @patch('test_gemini.test_image_generation')
    @patch('test_gemini.test_gemini_connection')
    def test_handles_image_generation_failure(self, mock_test_conn, mock_test_img):
        """Test handling of image generation failure"""
        mock_client = Mock()
        mock_test_conn.return_value = (True, mock_client)
        mock_test_img.return_value = False
        
        # Should not raise exception
        test_gemini.main()
        
        mock_test_img.assert_called_once_with(mock_client)
    
    @patch('test_gemini.test_image_generation')
    @patch('test_gemini.test_gemini_connection')
    def test_both_tests_pass_successfully(self, mock_test_conn, mock_test_img):
        """Test successful completion of all tests"""
        mock_client = Mock()
        mock_test_conn.return_value = (True, mock_client)
        mock_test_img.return_value = True
        
        # Should complete without errors
        test_gemini.main()
        
        mock_test_conn.assert_called_once()
        mock_test_img.assert_called_once_with(mock_client)


class TestIntegration:
    """Integration tests for the test script"""
    
    @patch('test_gemini.PILImage')
    @patch('test_gemini.genai.Client')
    def test_full_successful_flow(self, mock_client_class, mock_pil_image):
        """Test complete successful execution flow"""
        # Setup mocks
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_img = Mock()
        mock_img.size = (1024, 1024)
        mock_img.mode = 'RGBA'
        mock_pil_image.open.return_value = mock_img
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            with patch('os.path.exists', return_value=True):
                test_gemini.main()
        
        # Verify all steps executed
        mock_client_class.assert_called_once()
        mock_client.models.generate_content.assert_called_once()
        mock_img.save.assert_called_once()
    
    @patch('test_gemini.genai.Client')
    def test_handles_missing_api_key(self, mock_client_class):
        """Test handling of missing API key in full flow"""
        with patch.dict('os.environ', {}, clear=True):
            # Should not raise exception
            test_gemini.main()
        
        # Client should not be created
        mock_client_class.assert_not_called()


class TestErrorRecovery:
    """Test error recovery and reporting"""
    
    @patch('test_gemini.PILImage')
    @patch('test_gemini.traceback.print_exc')
    def test_prints_traceback_on_exception(self, mock_traceback, mock_pil_image):
        """Test that tracebacks are printed for debugging"""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = Exception("Test error")
        
        result = test_gemini.test_image_generation(mock_client)
        
        assert result is False
        mock_traceback.assert_called_once()
    
    def test_validates_environment_cleanly(self):
        """Test clean validation of environment setup"""
        with patch.dict('os.environ', {}, clear=True):
            success, client = test_gemini.test_gemini_connection()
            
            # Should fail gracefully without exceptions
            assert success is False
            assert client is None


class TestOutputValidation:
    """Test output and reporting functionality"""
    
    @patch('test_gemini.PILImage')
    def test_reports_image_properties(self, mock_pil_image):
        """Test that image properties are reported"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        # Create mock image with specific properties
        mock_img = Mock()
        mock_img.size = (1024, 1024)
        mock_img.mode = 'RGBA'
        mock_pil_image.open.return_value = mock_img
        
        with patch('os.path.exists', return_value=True):
            result = test_gemini.test_image_generation(mock_client)
        
        assert result is True
        # Image properties should be accessible
        assert mock_img.size == (1024, 1024)
        assert mock_img.mode == 'RGBA'


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    @patch('test_gemini.PILImage')
    def test_handles_empty_image_data(self, mock_pil_image):
        """Test handling of empty image data"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b""
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_image.open.side_effect = Exception("Cannot identify image file")
        
        result = test_gemini.test_image_generation(mock_client)
        
        assert result is False
    
    @patch('test_gemini.PILImage')
    def test_handles_corrupted_image_data(self, mock_pil_image):
        """Test handling of corrupted image data"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"corrupted_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_image.open.side_effect = Exception("Image file is corrupted")
        
        result = test_gemini.test_image_generation(mock_client)
        
        assert result is False
    
    def test_handles_very_long_api_key(self):
        """Test handling of very long API key"""
        very_long_key = "a" * 1000
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': very_long_key}):
            with patch('test_gemini.genai.Client') as mock_client_class:
                mock_client_class.return_value = Mock()
                
                success, client = test_gemini.test_gemini_connection()
                
                assert success is True
                mock_client_class.assert_called_once_with(api_key=very_long_key)


class TestPromptConstruction:
    """Test prompt construction for image generation"""
    
    @patch('test_gemini.PILImage')
    def test_prompt_includes_size_specification(self, mock_pil_image):
        """Test that prompt includes specific size requirements"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_img = Mock()
        mock_img.size = (111, 101)
        mock_img.mode = 'RGBA'
        mock_pil_image.open.return_value = mock_img
        
        with patch('os.path.exists', return_value=True):
            test_gemini.test_image_generation(mock_client)
        
        prompt = mock_client.models.generate_content.call_args[1]['contents']
        assert '111x101' in prompt
    
    @patch('test_gemini.PILImage')
    def test_prompt_specifies_style_requirements(self, mock_pil_image):
        """Test that prompt specifies style requirements"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_img = Mock()
        mock_img.size = (111, 101)
        mock_img.mode = 'RGBA'
        mock_pil_image.open.return_value = mock_img
        
        with patch('os.path.exists', return_value=True):
            test_gemini.test_image_generation(mock_client)
        
        prompt = mock_client.models.generate_content.call_args[1]['contents']
        assert '8-bit' in prompt.lower() or 'pixel art' in prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])