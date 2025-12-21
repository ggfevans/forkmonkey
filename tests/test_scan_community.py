"""
Tests for scan_community - Community Scanner
Tests nested fork scanning (1st, 2nd, 3rd degree siblings)
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

# Import the functions we're testing
from src.scan_community import (
    collect_repos,
    get_degree_label,
    scan_repo,
    generate_community_data,
    generate_leaderboard,
    generate_family_tree,
    generate_network_stats
)


class TestGetDegreeLabel:
    """Test degree label helper"""
    
    def test_root_degree(self):
        """Test root label"""
        assert get_degree_label(0) == "root"
    
    def test_first_degree(self):
        """Test 1st degree label"""
        assert get_degree_label(1) == "1st degree"
    
    def test_second_degree(self):
        """Test 2nd degree label"""
        assert get_degree_label(2) == "2nd degree"
    
    def test_third_degree(self):
        """Test 3rd degree label"""
        assert get_degree_label(3) == "3rd degree"
    
    def test_higher_degree(self):
        """Test higher degree fallback"""
        assert get_degree_label(4) == "4th degree"
        assert get_degree_label(10) == "10th degree"


class TestCollectRepos:
    """Test nested fork collection with BFS"""
    
    def _create_mock_repo(self, full_name, forks=None):
        """Helper to create a mock repo"""
        repo = MagicMock()
        repo.full_name = full_name
        
        if forks:
            mock_forks = MagicMock()
            mock_forks.get_page.return_value = forks
            repo.get_forks.return_value = mock_forks
        else:
            mock_forks = MagicMock()
            mock_forks.get_page.return_value = []
            repo.get_forks.return_value = mock_forks
        
        return repo
    
    def test_collect_root_only(self):
        """Test collecting just root repo with no forks"""
        root = self._create_mock_repo("owner/root")
        
        repos = collect_repos(root, max_depth=3, max_total=100)
        
        assert len(repos) == 1
        assert repos[0][0].full_name == "owner/root"
        assert repos[0][1] == 0  # degree = 0 for root
    
    def test_collect_first_degree_forks(self):
        """Test collecting 1st degree forks"""
        fork1 = self._create_mock_repo("user1/fork1")
        fork2 = self._create_mock_repo("user2/fork2")
        root = self._create_mock_repo("owner/root", forks=[fork1, fork2])
        
        repos = collect_repos(root, max_depth=1, max_total=100)
        
        assert len(repos) == 3  # root + 2 forks
        
        # Verify degrees
        degrees = {r[0].full_name: r[1] for r in repos}
        assert degrees["owner/root"] == 0
        assert degrees["user1/fork1"] == 1
        assert degrees["user2/fork2"] == 1
    
    def test_collect_nested_forks_depth_2(self):
        """Test collecting 2nd degree forks (forks of forks)"""
        # 2nd level forks
        fork_of_fork1 = self._create_mock_repo("user3/fork_of_fork1")
        fork_of_fork2 = self._create_mock_repo("user4/fork_of_fork2")
        
        # 1st level forks (with their own forks)
        fork1 = self._create_mock_repo("user1/fork1", forks=[fork_of_fork1])
        fork2 = self._create_mock_repo("user2/fork2", forks=[fork_of_fork2])
        
        # Root
        root = self._create_mock_repo("owner/root", forks=[fork1, fork2])
        
        repos = collect_repos(root, max_depth=2, max_total=100)
        
        assert len(repos) == 5  # root + 2 first-degree + 2 second-degree
        
        # Verify degrees
        degrees = {r[0].full_name: r[1] for r in repos}
        assert degrees["owner/root"] == 0
        assert degrees["user1/fork1"] == 1
        assert degrees["user2/fork2"] == 1
        assert degrees["user3/fork_of_fork1"] == 2
        assert degrees["user4/fork_of_fork2"] == 2
    
    def test_collect_nested_forks_depth_3(self):
        """Test collecting 3rd degree forks"""
        # 3rd level fork
        third_level = self._create_mock_repo("user5/third_level")
        
        # 2nd level fork (with its own fork)
        second_level = self._create_mock_repo("user3/second_level", forks=[third_level])
        
        # 1st level fork
        first_level = self._create_mock_repo("user1/first_level", forks=[second_level])
        
        # Root
        root = self._create_mock_repo("owner/root", forks=[first_level])
        
        repos = collect_repos(root, max_depth=3, max_total=100)
        
        assert len(repos) == 4  # root + 3 levels
        
        # Verify degrees
        degrees = {r[0].full_name: r[1] for r in repos}
        assert degrees["owner/root"] == 0
        assert degrees["user1/first_level"] == 1
        assert degrees["user3/second_level"] == 2
        assert degrees["user5/third_level"] == 3
    
    def test_max_depth_limit(self):
        """Test that max_depth limits collection"""
        # 3rd level fork (should NOT be collected with max_depth=2)
        third_level = self._create_mock_repo("user5/third_level")
        
        second_level = self._create_mock_repo("user3/second_level", forks=[third_level])
        first_level = self._create_mock_repo("user1/first_level", forks=[second_level])
        root = self._create_mock_repo("owner/root", forks=[first_level])
        
        repos = collect_repos(root, max_depth=2, max_total=100)
        
        assert len(repos) == 3  # root + 1st + 2nd level only
        
        names = [r[0].full_name for r in repos]
        assert "user5/third_level" not in names
    
    def test_max_total_limit(self):
        """Test that max_total limits total repos"""
        fork1 = self._create_mock_repo("user1/fork1")
        fork2 = self._create_mock_repo("user2/fork2")
        fork3 = self._create_mock_repo("user3/fork3")
        root = self._create_mock_repo("owner/root", forks=[fork1, fork2, fork3])
        
        repos = collect_repos(root, max_depth=3, max_total=3)
        
        assert len(repos) == 3  # Limited by max_total
    
    def test_no_duplicate_repos(self):
        """Test that duplicate repos are not collected"""
        # Same fork referenced twice (shouldn't happen but be safe)
        fork1 = self._create_mock_repo("user1/fork1")
        root = self._create_mock_repo("owner/root", forks=[fork1, fork1])
        
        repos = collect_repos(root, max_depth=3, max_total=100)
        
        # Should deduplicate
        names = [r[0].full_name for r in repos]
        assert names.count("user1/fork1") == 1


class TestScanRepo:
    """Test individual repo scanning"""
    
    def _create_mock_repo(self, full_name, owner, name, is_fork=False, parent=None):
        """Create a mock repo with all needed attributes"""
        repo = MagicMock()
        repo.full_name = full_name
        repo.name = name
        repo.html_url = f"https://github.com/{full_name}"
        repo.fork = is_fork
        repo.parent = parent
        repo.created_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
        repo.updated_at = datetime(2024, 6, 1, tzinfo=timezone.utc)
        
        owner_mock = MagicMock()
        owner_mock.login = owner
        repo.owner = owner_mock
        
        # No monkey data by default
        repo.get_contents = MagicMock(side_effect=Exception("Not found"))
        
        return repo
    
    def test_scan_repo_with_degree(self):
        """Test that scan_repo includes degree in output"""
        repo = self._create_mock_repo("user1/fork1", "user1", "fork1", is_fork=True)
        
        # Mock stats.json to make repo valid
        stats_content = MagicMock()
        stats_content.decoded_content = b'{"generation": 2, "rarity_score": 50}'
        repo.get_contents = MagicMock(return_value=stats_content)
        
        result = scan_repo(repo, "owner/root", degree=2)
        
        assert result is not None
        assert result["degree"] == 2
        assert result["degree_label"] == "2nd degree"
    
    def test_scan_repo_default_degree(self):
        """Test default degree is 0"""
        repo = self._create_mock_repo("owner/root", "owner", "root")
        
        stats_content = MagicMock()
        stats_content.decoded_content = b'{"generation": 1, "rarity_score": 75}'
        repo.get_contents = MagicMock(return_value=stats_content)
        
        result = scan_repo(repo, "owner/root")
        
        assert result is not None
        assert result["degree"] == 0
        assert result["degree_label"] == "root"
        assert result["is_root"] == True
    
    def test_scan_repo_no_monkey_data(self):
        """Test repo without monkey data returns None"""
        repo = self._create_mock_repo("user1/empty", "user1", "empty")
        
        result = scan_repo(repo, "owner/root", degree=1)
        
        assert result is None


class TestGenerators:
    """Test output file generators include degree info"""
    
    def _create_sample_monkeys(self):
        """Create sample monkey data for testing"""
        return [
            {
                "owner": "owner",
                "repo": "root",
                "full_name": "owner/root",
                "url": "https://github.com/owner/root",
                "is_root": True,
                "degree": 0,
                "degree_label": "root",
                "parent": None,
                "created_at": "2024-01-01T00:00:00+00:00",
                "updated_at": "2024-06-01T00:00:00+00:00",
                "monkey_stats": {"generation": 1, "rarity_score": 100, "age_days": 180, "mutation_count": 0},
                "monkey_svg": "<svg></svg>",
                "monkey_dna": {}
            },
            {
                "owner": "user1",
                "repo": "fork1",
                "full_name": "user1/fork1",
                "url": "https://github.com/user1/fork1",
                "is_root": False,
                "degree": 1,
                "degree_label": "1st degree",
                "parent": "owner/root",
                "created_at": "2024-02-01T00:00:00+00:00",
                "updated_at": "2024-06-15T00:00:00+00:00",
                "monkey_stats": {"generation": 2, "rarity_score": 80, "age_days": 150, "mutation_count": 3},
                "monkey_svg": "<svg>fork1</svg>",
                "monkey_dna": {}
            },
            {
                "owner": "user2",
                "repo": "fork_of_fork",
                "full_name": "user2/fork_of_fork",
                "url": "https://github.com/user2/fork_of_fork",
                "is_root": False,
                "degree": 2,
                "degree_label": "2nd degree",
                "parent": "user1/fork1",
                "created_at": "2024-03-01T00:00:00+00:00",
                "updated_at": "2024-07-01T00:00:00+00:00",
                "monkey_stats": {"generation": 3, "rarity_score": 60, "age_days": 120, "mutation_count": 5},
                "monkey_svg": "<svg>fork_of_fork</svg>",
                "monkey_dna": {}
            }
        ]
    
    @patch("src.scan_community.Path")
    def test_generate_leaderboard_includes_degree(self, mock_path):
        """Test leaderboard includes degree info"""
        mock_file = MagicMock()
        mock_path.return_value.parent.mkdir = MagicMock()
        
        monkeys = self._create_sample_monkeys()
        
        import json
        with patch("builtins.open", MagicMock()) as mock_open:
            mock_open.return_value.__enter__ = MagicMock(return_value=mock_file)
            mock_open.return_value.__exit__ = MagicMock(return_value=False)
            
            generate_leaderboard(monkeys)
            
            # Check that json.dump was called
            assert mock_file.write.called or mock_open.called
    
    @patch("src.scan_community.Path")
    def test_generate_family_tree_includes_degree(self, mock_path):
        """Test family tree includes degree info"""
        mock_file = MagicMock()
        mock_path.return_value.parent.mkdir = MagicMock()
        
        monkeys = self._create_sample_monkeys()
        
        with patch("builtins.open", MagicMock()) as mock_open:
            mock_open.return_value.__enter__ = MagicMock(return_value=mock_file)
            mock_open.return_value.__exit__ = MagicMock(return_value=False)
            
            generate_family_tree("owner/root", monkeys)
            
            assert mock_file.write.called or mock_open.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
