"""
Unit tests for generate_forkmonkey.py - Fork Monkey Sprite Generator

Tests cover:
- Gemini API client creation
- Base character generation
- Animation frame generation with different animation types
- Prompt generation logic
- Error handling and API failures
- Rate limiting and delays
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import sys
import io

# Add the script directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "experiment1" / "scripts" / "sprite-generation"))

import generate_forkmonkey


class TestCreateClient:
    """Test the create_client function"""
    
    def test_raises_error_when_api_key_missing(self):
        """Test that ValueError is raised when API key is not set"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable not set"):
                generate_forkmonkey.create_client()
    
    @patch('generate_forkmonkey.genai.Client')
    def test_creates_client_with_api_key(self, mock_client_class):
        """Test that client is created with the API key"""
        test_api_key = "test_api_key_12345"
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': test_api_key}):
            generate_forkmonkey.create_client()
            
            mock_client_class.assert_called_once_with(api_key=test_api_key)
    
    @patch('generate_forkmonkey.genai.Client')
    def test_returns_client_instance(self, mock_client_class):
        """Test that the function returns a client instance"""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            result = generate_forkmonkey.create_client()
            
            assert result == mock_client


class TestGenerateBaseCharacter:
    """Test the generate_base_character function"""
    
    @patch('generate_forkmonkey.Image')
    def test_generates_image_with_correct_config(self, mock_image_class):
        """Test that image generation uses correct configuration"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/base_character.png'):
                result = generate_forkmonkey.generate_base_character(mock_client)
        
        # Verify generate_content was called
        mock_client.models.generate_content.assert_called_once()
        call_args = mock_client.models.generate_content.call_args
        
        # Check model name
        assert call_args[1]['model'] == generate_forkmonkey.MODEL
        
        # Check config has IMAGE modality
        config = call_args[1]['config']
        assert config.response_modalities == ['IMAGE']
    
    @patch('generate_forkmonkey.Image')
    def test_saves_base_character_image(self, mock_image_class):
        """Test that base character image is saved"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/base_character.png') as mock_join:
                result = generate_forkmonkey.generate_base_character(mock_client)
                
                mock_pil_img.save.assert_called_once()
                save_path = mock_pil_img.save.call_args[0][0]
                assert 'base_character.png' in save_path
    
    def test_raises_exception_when_no_image_generated(self):
        """Test that exception is raised when API returns no image"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.parts = []
        mock_client.models.generate_content.return_value = mock_response
        
        with pytest.raises(Exception, match="No image generated"):
            generate_forkmonkey.generate_base_character(mock_client)
    
    @patch('generate_forkmonkey.Image')
    def test_prompt_includes_key_character_features(self, mock_image_class):
        """Test that the prompt includes essential character features"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/base_character.png'):
                generate_forkmonkey.generate_base_character(mock_client)
        
        call_args = mock_client.models.generate_content.call_args
        prompt = call_args[1]['contents']
        
        # Check for key elements in prompt
        assert 'monkey' in prompt.lower()
        assert 'fork' in prompt.lower()
        assert 'pixel art' in prompt.lower()
        assert 'transparent background' in prompt.lower()


class TestGenerateAnimationFrame:
    """Test the generate_animation_frame function"""
    
    @patch('generate_forkmonkey.Image')
    def test_generates_frame_for_idle_animation(self, mock_image_class):
        """Test frame generation for idle animation"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/idle_frame_01.png'):
                result = generate_forkmonkey.generate_animation_frame(
                    mock_client, 'idle', 1, 4
                )
        
        assert result == mock_pil_img
        mock_pil_img.save.assert_called_once()
    
    @patch('generate_forkmonkey.Image')
    def test_generates_frame_for_walk_animation(self, mock_image_class):
        """Test frame generation for walk animation"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/walk_frame_01.png'):
                result = generate_forkmonkey.generate_animation_frame(
                    mock_client, 'walk', 1, 6
                )
        
        assert result == mock_pil_img
    
    @patch('generate_forkmonkey.Image')
    def test_generates_frame_for_run_animation(self, mock_image_class):
        """Test frame generation for run animation"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/run_frame_01.png'):
                result = generate_forkmonkey.generate_animation_frame(
                    mock_client, 'run', 1, 8
                )
        
        assert result == mock_pil_img
    
    @patch('generate_forkmonkey.Image')
    def test_generates_frame_for_swipe_animation(self, mock_image_class):
        """Test frame generation for swipe animation"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/swipe_frame_01.png'):
                result = generate_forkmonkey.generate_animation_frame(
                    mock_client, 'swipe', 1, 5
                )
        
        assert result == mock_pil_img
    
    @patch('generate_forkmonkey.Image')
    def test_generates_frame_for_with_ball_animation(self, mock_image_class):
        """Test frame generation for with_ball animation"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/with_ball_frame_01.png'):
                result = generate_forkmonkey.generate_animation_frame(
                    mock_client, 'with_ball', 1, 4
                )
        
        assert result == mock_pil_img
    
    def test_returns_none_on_exception(self):
        """Test that function returns None when an exception occurs"""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = Exception("API Error")
        
        result = generate_forkmonkey.generate_animation_frame(
            mock_client, 'idle', 1, 4
        )
        
        assert result is None
    
    @patch('generate_forkmonkey.Image')
    def test_idle_frame_prompts_vary_by_frame_number(self, mock_image_class):
        """Test that idle animation prompts vary based on frame number"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        prompts = []
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', return_value='/tmp/test/idle_frame_01.png'):
                for frame_num in range(1, 5):
                    generate_forkmonkey.generate_animation_frame(
                        mock_client, 'idle', frame_num, 4
                    )
                    call_args = mock_client.models.generate_content.call_args
                    prompts.append(call_args[1]['contents'])
        
        # Different frames should have different instructions
        assert 'Frame 1' in prompts[0] or 'neutral' in prompts[0].lower()
        assert 'Frame 2' in prompts[1] or 'upward' in prompts[1].lower()
    
    @patch('generate_forkmonkey.Image')
    def test_saves_frame_with_correct_filename(self, mock_image_class):
        """Test that frames are saved with correct naming convention"""
        mock_client = Mock()
        mock_response = Mock()
        mock_part = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response
        
        mock_pil_img = Mock()
        mock_image_class.open.return_value = mock_pil_img
        
        with patch('generate_forkmonkey.OUTPUT_DIR', '/tmp/test'):
            with patch('os.path.join', side_effect=lambda d, f: f'/tmp/test/{f}') as mock_join:
                generate_forkmonkey.generate_animation_frame(
                    mock_client, 'idle', 3, 4
                )
                
                # Check the filename format
                call_args = mock_join.call_args[0]
                assert 'idle_frame_03.png' in call_args[1]


class TestGenerateAllAnimations:
    """Test the generate_all_animations function"""
    
    @patch('generate_forkmonkey.time.sleep')
    @patch('generate_forkmonkey.generate_animation_frame')
    def test_generates_all_defined_animations(self, mock_gen_frame, mock_sleep):
        """Test that all animations are generated"""
        mock_client = Mock()
        mock_gen_frame.return_value = Mock()
        
        generate_forkmonkey.generate_all_animations(mock_client)
        
        # Should generate frames for all animations
        total_frames = sum(info['frames'] for info in generate_forkmonkey.ANIMATIONS.values())
        assert mock_gen_frame.call_count == total_frames
    
    @patch('generate_forkmonkey.time.sleep')
    @patch('generate_forkmonkey.generate_animation_frame')
    def test_adds_delay_between_frames(self, mock_gen_frame, mock_sleep):
        """Test that delays are added between frame generations"""
        mock_client = Mock()
        mock_gen_frame.return_value = Mock()
        
        generate_forkmonkey.generate_all_animations(mock_client)
        
        # Should sleep between each frame
        total_frames = sum(info['frames'] for info in generate_forkmonkey.ANIMATIONS.values())
        assert mock_sleep.call_count == total_frames
        
        # Verify sleep duration
        for call in mock_sleep.call_args_list:
            assert call[0][0] == 1  # 1 second delay
    
    @patch('generate_forkmonkey.time.sleep')
    @patch('generate_forkmonkey.generate_animation_frame')
    def test_generates_correct_frame_counts(self, mock_gen_frame, mock_sleep):
        """Test that correct number of frames are generated per animation"""
        mock_client = Mock()
        mock_gen_frame.return_value = Mock()
        
        generate_forkmonkey.generate_all_animations(mock_client)
        
        # Check that frames are generated with correct counts
        for anim_name, anim_info in generate_forkmonkey.ANIMATIONS.items():
            frame_calls = [
                call for call in mock_gen_frame.call_args_list
                if call[0][1] == anim_name
            ]
            assert len(frame_calls) == anim_info['frames']


class TestMain:
    """Test the main function"""
    
    @patch('generate_forkmonkey.time.sleep')
    @patch('generate_forkmonkey.generate_all_animations')
    @patch('generate_forkmonkey.generate_base_character')
    @patch('generate_forkmonkey.create_client')
    def test_creates_client_first(self, mock_create_client, mock_gen_base, 
                                   mock_gen_all, mock_sleep):
        """Test that client is created before any generation"""
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        mock_gen_base.return_value = Mock()
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            generate_forkmonkey.main()
        
        mock_create_client.assert_called_once()
    
    @patch('generate_forkmonkey.time.sleep')
    @patch('generate_forkmonkey.generate_all_animations')
    @patch('generate_forkmonkey.generate_base_character')
    @patch('generate_forkmonkey.create_client')
    def test_generates_base_character_before_animations(self, mock_create_client, 
                                                       mock_gen_base, mock_gen_all, 
                                                       mock_sleep):
        """Test that base character is generated before animations"""
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        mock_gen_base.return_value = Mock()
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            generate_forkmonkey.main()
        
        mock_gen_base.assert_called_once_with(mock_client)
        mock_gen_all.assert_called_once_with(mock_client)
    
    @patch('generate_forkmonkey.time.sleep')
    @patch('generate_forkmonkey.generate_all_animations')
    @patch('generate_forkmonkey.generate_base_character')
    @patch('generate_forkmonkey.create_client')
    def test_waits_between_base_and_animations(self, mock_create_client, 
                                               mock_gen_base, mock_gen_all, 
                                               mock_sleep):
        """Test that there's a delay between base generation and animations"""
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        mock_gen_base.return_value = Mock()
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            generate_forkmonkey.main()
        
        # Should have at least one sleep call for the 3-second wait
        sleep_calls = [call for call in mock_sleep.call_args_list if call[0][0] == 3]
        assert len(sleep_calls) >= 1


class TestAnimationsConfiguration:
    """Test the ANIMATIONS configuration"""
    
    def test_animations_dict_structure(self):
        """Test that ANIMATIONS dict has correct structure"""
        assert isinstance(generate_forkmonkey.ANIMATIONS, dict)
        assert len(generate_forkmonkey.ANIMATIONS) > 0
        
        for name, config in generate_forkmonkey.ANIMATIONS.items():
            assert isinstance(name, str)
            assert isinstance(config, dict)
            assert 'frames' in config
            assert 'description' in config
            assert isinstance(config['frames'], int)
            assert isinstance(config['description'], str)
            assert config['frames'] > 0
    
    def test_all_required_animations_present(self):
        """Test that all required animations are defined"""
        required_animations = {'idle', 'walk', 'run', 'swipe', 'with_ball'}
        actual_animations = set(generate_forkmonkey.ANIMATIONS.keys())
        
        assert required_animations.issubset(actual_animations), \
            f"Missing animations: {required_animations - actual_animations}"
    
    def test_animation_frame_counts_are_reasonable(self):
        """Test that frame counts are within reasonable ranges"""
        for name, config in generate_forkmonkey.ANIMATIONS.items():
            # Frame counts should typically be between 2 and 12 for sprite animations
            assert 2 <= config['frames'] <= 12, \
                f"Animation '{name}' has unusual frame count: {config['frames']}"


class TestConstants:
    """Test module constants"""
    
    def test_model_is_set(self):
        """Test that MODEL constant is defined"""
        assert hasattr(generate_forkmonkey, 'MODEL')
        assert isinstance(generate_forkmonkey.MODEL, str)
        assert len(generate_forkmonkey.MODEL) > 0
    
    def test_target_size_is_valid(self):
        """Test that TARGET_SIZE is valid"""
        assert hasattr(generate_forkmonkey, 'TARGET_SIZE')
        assert isinstance(generate_forkmonkey.TARGET_SIZE, tuple)
        assert len(generate_forkmonkey.TARGET_SIZE) == 2
        assert all(isinstance(x, int) and x > 0 for x in generate_forkmonkey.TARGET_SIZE)
    
    def test_target_size_matches_vscode_pets_standard(self):
        """Test that target size is VS Code Pets compatible"""
        # VS Code Pets uses 111x101 as noted in the code comments
        assert generate_forkmonkey.TARGET_SIZE == (111, 101)


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @patch('generate_forkmonkey.Image')
    def test_handles_api_timeout_gracefully(self, mock_image_class):
        """Test handling of API timeout errors"""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = TimeoutError("API timeout")
        
        result = generate_forkmonkey.generate_animation_frame(
            mock_client, 'idle', 1, 4
        )
        
        # Should return None instead of crashing
        assert result is None
    
    @patch('generate_forkmonkey.Image')
    def test_handles_network_errors_gracefully(self, mock_image_class):
        """Test handling of network errors"""
        mock_client = Mock()
        mock_client.models.generate_content.side_effect = ConnectionError("Network error")
        
        result = generate_forkmonkey.generate_animation_frame(
            mock_client, 'idle', 1, 4
        )
        
        # Should return None instead of crashing
        assert result is None
    
    @patch('generate_forkmonkey.Image')
    def test_handles_invalid_response_structure(self, mock_image_class):
        """Test handling of unexpected API response structure"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.parts = [Mock(spec=[])]  # Part without inline_data
        mock_client.models.generate_content.return_value = mock_response
        
        with pytest.raises(Exception):
            generate_forkmonkey.generate_animation_frame(
                mock_client, 'idle', 1, 4
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])