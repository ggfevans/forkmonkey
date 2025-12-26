"""
Unit tests for JSON data files validation

Tests cover:
- web/community_data.json
- web/family_tree.json
- web/leaderboard.json
- web/network_stats.json

Validates:
- JSON structure and schema
- Required fields presence
- Data type correctness
- Value constraints and ranges
- Referential integrity
- Data consistency
"""

import pytest
import json
from pathlib import Path
from datetime import datetime


class TestCommunityDataJSON:
    """Test community_data.json structure and content"""
    
    @pytest.fixture
    def community_data(self):
        """Load community_data.json"""
        json_path = Path('web/community_data.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    
    def test_has_required_top_level_fields(self, community_data):
        """Test that all required top-level fields are present"""
        required_fields = ['last_updated', 'source_repo', 'total_forks', 'forks']
        
        for field in required_fields:
            assert field in community_data, f"Missing required field: {field}"
    
    def test_last_updated_is_valid_iso_format(self, community_data):
        """Test that last_updated is in valid ISO format"""
        last_updated = community_data['last_updated']
        
        # Should be able to parse as ISO format datetime
        try:
            datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
        except ValueError as e:
            pytest.fail(f"Invalid ISO datetime format: {e}")
    
    def test_total_forks_is_positive_integer(self, community_data):
        """Test that total_forks is a positive integer"""
        total_forks = community_data['total_forks']
        
        assert isinstance(total_forks, int), "total_forks should be an integer"
        assert total_forks >= 0, "total_forks should be non-negative"
    
    def test_total_forks_matches_forks_list_length(self, community_data):
        """Test that total_forks matches the length of forks array"""
        total_forks = community_data['total_forks']
        forks_list = community_data['forks']
        
        assert len(forks_list) == total_forks, \
            f"Forks list length ({len(forks_list)}) doesn't match total_forks ({total_forks})"
    
    def test_each_fork_has_required_fields(self, community_data):
        """Test that each fork entry has all required fields"""
        required_fork_fields = [
            'owner', 'repo', 'full_name', 'url', 'is_root', 
            'degree', 'degree_label', 'parent', 'created_at', 
            'updated_at', 'monkey_stats'
        ]
        
        for i, fork in enumerate(community_data['forks']):
            for field in required_fork_fields:
                assert field in fork, \
                    f"Fork {i} ({fork.get('full_name', 'unknown')}) missing field: {field}"
    
    def test_fork_urls_are_valid(self, community_data):
        """Test that fork URLs follow GitHub URL pattern"""
        for fork in community_data['forks']:
            url = fork['url']
            assert url.startswith('https://github.com/'), \
                f"Invalid GitHub URL: {url}"
            assert fork['owner'] in url and fork['repo'] in url, \
                f"URL doesn't match owner/repo: {url}"
    
    def test_full_name_format(self, community_data):
        """Test that full_name follows owner/repo format"""
        for fork in community_data['forks']:
            full_name = fork['full_name']
            assert '/' in full_name, f"Invalid full_name format: {full_name}"
            
            owner, repo = full_name.split('/', 1)
            assert owner == fork['owner'], f"Owner mismatch in {full_name}"
            assert repo == fork['repo'], f"Repo mismatch in {full_name}"
    
    def test_root_fork_properties(self, community_data):
        """Test that root fork has correct properties"""
        root_forks = [f for f in community_data['forks'] if f['is_root']]
        
        assert len(root_forks) == 1, "Should have exactly one root fork"
        
        root = root_forks[0]
        assert root['degree'] == 0, "Root should have degree 0"
        assert root['degree_label'] == 'root', "Root should have label 'root'"
        assert root['parent'] is None, "Root should have no parent"
    
    def test_degree_values_are_valid(self, community_data):
        """Test that degree values are non-negative integers"""
        for fork in community_data['forks']:
            degree = fork['degree']
            assert isinstance(degree, int), f"Degree should be integer: {fork['full_name']}"
            assert degree >= 0, f"Degree should be non-negative: {fork['full_name']}"
    
    def test_monkey_stats_structure(self, community_data):
        """Test that monkey_stats has required fields"""
        required_stats_fields = [
            'dna_hash', 'generation', 'age_days', 'mutation_count',
            'rarity_score', 'parent_id', 'traits'
        ]
        
        for fork in community_data['forks']:
            stats = fork['monkey_stats']
            for field in required_stats_fields:
                assert field in stats, \
                    f"Fork {fork['full_name']} monkey_stats missing: {field}"
    
    def test_traits_structure(self, community_data):
        """Test that traits have correct structure"""
        required_trait_categories = [
            'body_color', 'face_expression', 'accessory',
            'pattern', 'background', 'special'
        ]
        
        for fork in community_data['forks']:
            traits = fork['monkey_stats']['traits']
            
            for category in required_trait_categories:
                assert category in traits, \
                    f"Fork {fork['full_name']} missing trait category: {category}"
                
                trait = traits[category]
                assert 'value' in trait, f"Trait {category} missing 'value'"
                assert 'rarity' in trait, f"Trait {category} missing 'rarity'"
    
    def test_rarity_values_are_valid(self, community_data):
        """Test that rarity values are from valid set"""
        valid_rarities = {'common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'}
        
        for fork in community_data['forks']:
            traits = fork['monkey_stats']['traits']
            for category, trait in traits.items():
                rarity = trait['rarity']
                assert rarity in valid_rarities, \
                    f"Invalid rarity '{rarity}' in {fork['full_name']}, {category}"
    
    def test_generation_values_are_positive(self, community_data):
        """Test that generation values are positive integers"""
        for fork in community_data['forks']:
            generation = fork['monkey_stats']['generation']
            assert isinstance(generation, int), \
                f"Generation should be integer: {fork['full_name']}"
            assert generation > 0, \
                f"Generation should be positive: {fork['full_name']}"
    
    def test_rarity_score_is_numeric(self, community_data):
        """Test that rarity_score is a valid number"""
        for fork in community_data['forks']:
            rarity_score = fork['monkey_stats']['rarity_score']
            assert isinstance(rarity_score, (int, float)), \
                f"Rarity score should be numeric: {fork['full_name']}"
            assert rarity_score >= 0, \
                f"Rarity score should be non-negative: {fork['full_name']}"


class TestFamilyTreeJSON:
    """Test family_tree.json structure and content"""
    
    @pytest.fixture
    def family_tree(self):
        """Load family_tree.json"""
        json_path = Path('web/family_tree.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    
    def test_has_required_top_level_fields(self, family_tree):
        """Test that all required top-level fields are present"""
        required_fields = ['last_updated', 'root', 'total_nodes', 'nodes']
        
        for field in required_fields:
            assert field in family_tree, f"Missing required field: {field}"
    
    def test_total_nodes_matches_nodes_list_length(self, family_tree):
        """Test that total_nodes matches the length of nodes array"""
        total_nodes = family_tree['total_nodes']
        nodes_list = family_tree['nodes']
        
        assert len(nodes_list) == total_nodes, \
            f"Nodes list length ({len(nodes_list)}) doesn't match total_nodes ({total_nodes})"
    
    def test_each_node_has_required_fields(self, family_tree):
        """Test that each node has all required fields"""
        required_node_fields = ['id', 'owner', 'repo', 'url', 'parent', 'children']
        
        for i, node in enumerate(family_tree['nodes']):
            for field in required_node_fields:
                assert field in node, \
                    f"Node {i} ({node.get('id', 'unknown')}) missing field: {field}"
    
    def test_root_node_exists(self, family_tree):
        """Test that root node is in the nodes list"""
        root_id = family_tree['root']
        node_ids = [node['id'] for node in family_tree['nodes']]
        
        assert root_id in node_ids, f"Root node {root_id} not found in nodes list"
    
    def test_root_node_has_no_parent(self, family_tree):
        """Test that root node has parent set to null"""
        root_id = family_tree['root']
        root_node = next((n for n in family_tree['nodes'] if n['id'] == root_id), None)
        
        assert root_node is not None, "Root node not found"
        assert root_node['parent'] is None, "Root node should have no parent"
    
    def test_children_are_valid_node_ids(self, family_tree):
        """Test that all children references are valid node IDs"""
        node_ids = set(node['id'] for node in family_tree['nodes'])
        
        for node in family_tree['nodes']:
            for child_id in node['children']:
                assert child_id in node_ids, \
                    f"Invalid child reference: {child_id} in node {node['id']}"
    
    def test_parent_child_relationships_are_consistent(self, family_tree):
        """Test that parent-child relationships are bidirectional"""
        # Build parent map
        parent_map = {node['id']: node['parent'] for node in family_tree['nodes']}
        
        for node in family_tree['nodes']:
            for child_id in node['children']:
                assert parent_map.get(child_id) == node['id'], \
                    f"Parent-child mismatch: {child_id} claims parent {parent_map.get(child_id)}, " \
                    f"but {node['id']} lists it as child"
    
    def test_no_circular_references(self, family_tree):
        """Test that there are no circular parent-child references"""
        def has_cycle(node_id, visited, rec_stack, parent_map):
            visited.add(node_id)
            rec_stack.add(node_id)
            
            parent = parent_map.get(node_id)
            if parent:
                if parent in rec_stack:
                    return True
                if parent not in visited:
                    if has_cycle(parent, visited, rec_stack, parent_map):
                        return True
            
            rec_stack.remove(node_id)
            return False
        
        parent_map = {node['id']: node['parent'] for node in family_tree['nodes']}
        visited = set()
        
        for node in family_tree['nodes']:
            if node['id'] not in visited:
                rec_stack = set()
                assert not has_cycle(node['id'], visited, rec_stack, parent_map), \
                    f"Circular reference detected involving {node['id']}"


class TestLeaderboardJSON:
    """Test leaderboard.json structure and content"""
    
    @pytest.fixture
    def leaderboard(self):
        """Load leaderboard.json"""
        json_path = Path('web/leaderboard.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    
    def test_has_required_top_level_fields(self, leaderboard):
        """Test that all required top-level fields are present"""
        required_fields = ['last_updated', 'total_ranked', 'rankings']
        
        for field in required_fields:
            assert field in leaderboard, f"Missing required field: {field}"
    
    def test_total_ranked_matches_rankings_length(self, leaderboard):
        """Test that total_ranked matches the length of rankings array"""
        total_ranked = leaderboard['total_ranked']
        rankings_list = leaderboard['rankings']
        
        assert len(rankings_list) == total_ranked, \
            f"Rankings list length ({len(rankings_list)}) doesn't match total_ranked ({total_ranked})"
    
    def test_each_ranking_has_required_fields(self, leaderboard):
        """Test that each ranking entry has all required fields"""
        required_ranking_fields = [
            'rank', 'owner', 'repo', 'full_name', 'url', 'rarity_score',
            'generation', 'age_days', 'mutation_count', 'is_root', 'degree', 'degree_label'
        ]
        
        for i, ranking in enumerate(leaderboard['rankings']):
            for field in required_ranking_fields:
                assert field in ranking, \
                    f"Ranking {i} ({ranking.get('full_name', 'unknown')}) missing field: {field}"
    
    def test_ranks_are_sequential(self, leaderboard):
        """Test that ranks are sequential starting from 1"""
        rankings = leaderboard['rankings']
        
        for i, ranking in enumerate(rankings):
            expected_rank = i + 1
            assert ranking['rank'] == expected_rank, \
                f"Rank mismatch at position {i}: expected {expected_rank}, got {ranking['rank']}"
    
    def test_rankings_sorted_by_rarity_score(self, leaderboard):
        """Test that rankings are sorted by rarity_score descending"""
        rankings = leaderboard['rankings']
        
        for i in range(len(rankings) - 1):
            current_score = rankings[i]['rarity_score']
            next_score = rankings[i + 1]['rarity_score']
            
            # Allow equal scores (tied rankings)
            assert current_score >= next_score, \
                f"Rankings not sorted: position {i} has score {current_score}, " \
                f"position {i+1} has score {next_score}"
    
    def test_rarity_scores_are_valid(self, leaderboard):
        """Test that rarity scores are valid numbers"""
        for ranking in leaderboard['rankings']:
            rarity_score = ranking['rarity_score']
            assert isinstance(rarity_score, (int, float)), \
                f"Rarity score should be numeric: {ranking['full_name']}"
            assert rarity_score >= 0, \
                f"Rarity score should be non-negative: {ranking['full_name']}"
    
    def test_monkey_svg_is_present_when_included(self, leaderboard):
        """Test that monkey_svg field, if present, is a non-empty string"""
        for ranking in leaderboard['rankings']:
            if 'monkey_svg' in ranking:
                svg = ranking['monkey_svg']
                assert isinstance(svg, str), \
                    f"monkey_svg should be string: {ranking['full_name']}"
                assert len(svg) > 0, \
                    f"monkey_svg should not be empty: {ranking['full_name']}"
                assert '<svg' in svg, \
                    f"monkey_svg should contain SVG markup: {ranking['full_name']}"


class TestNetworkStatsJSON:
    """Test network_stats.json structure and content"""
    
    @pytest.fixture
    def network_stats(self):
        """Load network_stats.json"""
        json_path = Path('web/network_stats.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    
    def test_has_required_top_level_fields(self, network_stats):
        """Test that all required top-level fields are present"""
        required_fields = [
            'last_updated', 'total_monkeys', 'active_today', 'generations',
            'avg_rarity', 'max_rarity', 'min_rarity', 'rarest_trait',
            'most_common_trait', 'trait_distribution'
        ]
        
        for field in required_fields:
            assert field in network_stats, f"Missing required field: {field}"
    
    def test_counts_are_positive_integers(self, network_stats):
        """Test that count fields are positive integers"""
        assert isinstance(network_stats['total_monkeys'], int)
        assert network_stats['total_monkeys'] >= 0
        
        assert isinstance(network_stats['active_today'], int)
        assert network_stats['active_today'] >= 0
    
    def test_active_today_not_exceeds_total(self, network_stats):
        """Test that active_today doesn't exceed total_monkeys"""
        active = network_stats['active_today']
        total = network_stats['total_monkeys']
        
        assert active <= total, \
            f"active_today ({active}) cannot exceed total_monkeys ({total})"
    
    def test_generations_are_valid(self, network_stats):
        """Test that generations data is valid"""
        generations = network_stats['generations']
        
        assert isinstance(generations, dict), "generations should be a dictionary"
        
        for gen, count in generations.items():
            assert gen.isdigit(), f"Generation key should be numeric string: {gen}"
            assert isinstance(count, int), f"Generation count should be integer: {gen}"
            assert count > 0, f"Generation count should be positive: {gen}"
    
    def test_rarity_statistics_are_valid(self, network_stats):
        """Test that rarity statistics are valid numbers"""
        avg_rarity = network_stats['avg_rarity']
        max_rarity = network_stats['max_rarity']
        min_rarity = network_stats['min_rarity']
        
        assert isinstance(avg_rarity, (int, float)), "avg_rarity should be numeric"
        assert isinstance(max_rarity, (int, float)), "max_rarity should be numeric"
        assert isinstance(min_rarity, (int, float)), "min_rarity should be numeric"
        
        assert min_rarity <= avg_rarity <= max_rarity, \
            f"Rarity statistics order incorrect: min={min_rarity}, avg={avg_rarity}, max={max_rarity}"
    
    def test_rarest_trait_structure(self, network_stats):
        """Test that rarest_trait has correct structure"""
        rarest = network_stats['rarest_trait']
        
        required_fields = ['trait', 'value', 'count']
        for field in required_fields:
            assert field in rarest, f"rarest_trait missing field: {field}"
        
        assert isinstance(rarest['count'], int)
        assert rarest['count'] > 0
    
    def test_most_common_trait_structure(self, network_stats):
        """Test that most_common_trait has correct structure"""
        most_common = network_stats['most_common_trait']
        
        required_fields = ['trait', 'value', 'count']
        for field in required_fields:
            assert field in most_common, f"most_common_trait missing field: {field}"
        
        assert isinstance(most_common['count'], int)
        assert most_common['count'] > 0
    
    def test_trait_distribution_structure(self, network_stats):
        """Test that trait_distribution has correct structure"""
        distribution = network_stats['trait_distribution']
        
        expected_categories = [
            'body_color', 'face_expression', 'accessory',
            'pattern', 'background', 'special'
        ]
        
        for category in expected_categories:
            assert category in distribution, f"Missing trait category: {category}"
            
            category_data = distribution[category]
            assert isinstance(category_data, dict), \
                f"Category {category} should be a dictionary"
            
            for value, count in category_data.items():
                assert isinstance(count, int), \
                    f"Count for {category}/{value} should be integer"
                assert count > 0, \
                    f"Count for {category}/{value} should be positive"
    
    def test_trait_counts_sum_to_total(self, network_stats):
        """Test that trait counts sum to total_monkeys for each category"""
        total_monkeys = network_stats['total_monkeys']
        distribution = network_stats['trait_distribution']
        
        for category, values in distribution.items():
            category_sum = sum(values.values())
            assert category_sum == total_monkeys, \
                f"Trait category {category} sum ({category_sum}) doesn't match total_monkeys ({total_monkeys})"
    
    def test_rarest_trait_is_actually_rarest(self, network_stats):
        """Test that rarest_trait has the minimum count in its category"""
        rarest = network_stats['rarest_trait']
        distribution = network_stats['trait_distribution']
        
        category = rarest['trait']
        value = rarest['value']
        count = rarest['count']
        
        # Check if this count is indeed the minimum in the category
        category_counts = distribution[category].values()
        min_count = min(category_counts)
        
        assert count == min_count, \
            f"rarest_trait count ({count}) is not the minimum in category {category} ({min_count})"
    
    def test_most_common_trait_is_actually_most_common(self, network_stats):
        """Test that most_common_trait has the maximum count in its category"""
        most_common = network_stats['most_common_trait']
        distribution = network_stats['trait_distribution']
        
        category = most_common['trait']
        value = most_common['value']
        count = most_common['count']
        
        # Check if this count is indeed the maximum in the category
        category_counts = distribution[category].values()
        max_count = max(category_counts)
        
        assert count == max_count, \
            f"most_common_trait count ({count}) is not the maximum in category {category} ({max_count})"


class TestCrossFileConsistency:
    """Test consistency across multiple JSON files"""
    
    @pytest.fixture
    def all_data(self):
        """Load all JSON files"""
        return {
            'community': json.load(open('web/community_data.json')),
            'family_tree': json.load(open('web/family_tree.json')),
            'leaderboard': json.load(open('web/leaderboard.json')),
            'network_stats': json.load(open('web/network_stats.json'))
        }
    
    def test_total_counts_are_consistent(self, all_data):
        """Test that total counts are consistent across files"""
        community_total = all_data['community']['total_forks']
        family_tree_total = all_data['family_tree']['total_nodes']
        leaderboard_total = all_data['leaderboard']['total_ranked']
        network_total = all_data['network_stats']['total_monkeys']
        
        assert community_total == family_tree_total == leaderboard_total == network_total, \
            f"Total counts inconsistent: community={community_total}, family_tree={family_tree_total}, " \
            f"leaderboard={leaderboard_total}, network={network_total}"
    
    def test_generation_counts_match(self, all_data):
        """Test that generation counts in network_stats match actual data"""
        community_forks = all_data['community']['forks']
        network_generations = all_data['network_stats']['generations']
        
        # Count generations from community data
        actual_gen_counts = {}
        for fork in community_forks:
            gen = str(fork['monkey_stats']['generation'])
            actual_gen_counts[gen] = actual_gen_counts.get(gen, 0) + 1
        
        assert actual_gen_counts == network_generations, \
            f"Generation counts mismatch: actual={actual_gen_counts}, network_stats={network_generations}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])