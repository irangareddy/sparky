"""
Advanced Analytics Example for Sparky Robot
Demonstrates advanced analytics and movement quality assessment
"""

import asyncio
import logging
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the src directory to the path so we can import sparky modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sparky.core.connection import Go2Connection, WebRTCConnectionMethod
from sparky.core.data_collector import DataCollector
from sparky.core.stream_processor import StreamProcessor
from sparky.core.analytics_engine import AnalyticsEngine, MovementDirection, MovementQuality

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedAnalyticsDemo:
    """Advanced analytics demonstration"""
    
    def __init__(self):
        self.connection = None
        self.data_collector = None
        self.stream_processor = None
        self.analytics_engine = None
        self.movement_count = 0
        self.analysis_results = []
    
    async def run_demo(self, duration_seconds: int = 120):
        """Run the advanced analytics demo"""
        try:
            print("Advanced Starting Advanced Analytics Demo")
            print("=" * 60)
            
            # Setup connection and components
            await self.setup_components()
            
            # Run analysis tasks
            await self.run_analysis_tasks(duration_seconds)
            
            # Generate final report
            await self.generate_analysis_report()
            
        except Exception as e:
            logger.error(f"Error in analytics demo: {e}")
        finally:
            await self.cleanup()
    
    async def setup_components(self):
        """Setup all streaming and analytics components"""
        print("Connecting to robot...")
        
        # Try multiple connection methods
        for method, kwargs in [
            (WebRTCConnectionMethod.LocalAP, {}),
            (WebRTCConnectionMethod.LocalSTA, {"ip": "192.168.8.181"}),
        ]:
            self.connection = Go2Connection(method, **kwargs)
            if await self.connection.connect():
                print(f" Connected via {method}")
                break
        else:
            raise Exception("Failed to connect to robot")
        
        # Initialize components
        print("Setting up analytics pipeline...")
        self.data_collector = DataCollector(self.connection.conn, buffer_size=1000)
        self.stream_processor = StreamProcessor(self.data_collector, window_size=50)
        self.analytics_engine = AnalyticsEngine(self.data_collector, self.stream_processor)
        
        # Start all components
        await self.data_collector.start_collection()
        await self.stream_processor.start_processing()
        await self.analytics_engine.start_analysis()
        
        print(" Analytics pipeline ready!")
    
    async def run_analysis_tasks(self, duration_seconds: int):
        """Run various analysis tasks"""
        print(f"Target Running analytics for {duration_seconds} seconds...")
        print(" Move the robot to see detailed analytics in action!")
        print("-" * 60)
        
        # Periodic analysis task
        analysis_task = asyncio.create_task(self.periodic_analysis())
        
        # Movement monitoring task
        monitoring_task = asyncio.create_task(self.movement_monitoring())
        
        # Wait for duration
        await asyncio.sleep(duration_seconds)
        
        # Cancel tasks
        analysis_task.cancel()
        monitoring_task.cancel()
        
        try:
            await analysis_task
            await monitoring_task
        except asyncio.CancelledError:
            pass
    
    async def periodic_analysis(self):
        """Periodic analysis every 10 seconds"""
        try:
            while True:
                await asyncio.sleep(10)
                await self.perform_detailed_analysis()
        except asyncio.CancelledError:
            pass
    
    async def movement_monitoring(self):
        """Continuous movement monitoring"""
        try:
            last_direction = MovementDirection.STATIONARY
            last_quality = None
            
            while True:
                await asyncio.sleep(2)
                
                # Check current movement
                is_moving = await self.analytics_engine.is_robot_moving()
                direction = await self.analytics_engine.get_movement_direction()
                quality = await self.analytics_engine.get_movement_quality()
                
                # Report changes
                if direction != last_direction:
                    print(f"\nWalking Movement Direction Changed: {direction.value}")
                    last_direction = direction
                
                if quality != last_quality and quality is not None:
                    quality_emoji = {
                        MovementQuality.EXCELLENT: "🌟",
                        MovementQuality.GOOD: "👍",
                        MovementQuality.FAIR: "WARNING",
                        MovementQuality.POOR: "FAILED"
                    }
                    print(f"📏 Movement Quality: {quality_emoji.get(quality, '?')} {quality.value}")
                    last_quality = quality
                
        except asyncio.CancelledError:
            pass
    
    async def perform_detailed_analysis(self):
        """Perform detailed analysis and report results"""
        print(f"\n{'='*20} ANALYSIS REPORT {'='*20}")
        
        # Current status
        is_moving = await self.analytics_engine.is_robot_moving()
        direction = await self.analytics_engine.get_movement_direction()
        quality = await self.analytics_engine.get_movement_quality()
        
        print(f" Robot Status:")
        print(f"   Moving: {'Yes' if is_moving else 'No'}")
        print(f"   Direction: {direction.value}")
        print(f"   Quality: {quality.value if quality else 'N/A'}")
        
        # Recent performance analysis
        performance = await self.analytics_engine.analyze_recent_performance(30.0)
        if 'error' not in performance:
            metrics = performance['performance_metrics']
            print(f"\nData Performance Metrics (30s):")
            print(f"   Smoothness: {metrics['smoothness']['average']:.3f}")
            print(f"   Efficiency: {metrics['efficiency']['average']:.3f}")
            print(f"   Stability: {metrics['stability']['average']:.3f}")
            
            behavior = performance['behavior_summary']
            print(f"\n Behavior Analysis:")
            print(f"   Current: {behavior['current_behavior']}")
            if behavior['detected_patterns']:
                recent_patterns = behavior['detected_patterns'][-3:]
                print(f"   Recent Patterns: {', '.join(recent_patterns)}")
        
        # Stream metrics
        metrics = self.stream_processor.get_current_metrics()
        print(f"\n⚡ Real-time Metrics:")
        print(f"   Activity Level: {metrics.activity_level}")
        print(f"   Movement %: {metrics.movement_percentage:.1f}%")
        print(f"   Stability Trend: {metrics.stability_trend}")
        print(f"   System Health: {metrics.overall_health}")
        print(f"   Max Motor Temp: {metrics.max_motor_temperature:.1f}°C")
        
        # Movement history
        movement_history = self.analytics_engine.get_movement_history(5)
        if movement_history:
            print(f"\nStatus Recent Movement Analysis:")
            for i, analysis in enumerate(movement_history[-3:]):
                print(f"   #{i+1}: {analysis.direction.value} - {analysis.quality.value} "
                      f"(conf: {analysis.confidence:.2f})")
        
        # Store results for final report
        self.analysis_results.append({
            'timestamp': datetime.now().isoformat(),
            'is_moving': is_moving,
            'direction': direction.value,
            'quality': quality.value if quality else None,
            'performance': performance,
            'metrics': {
                'activity_level': metrics.activity_level,
                'movement_percentage': metrics.movement_percentage,
                'stability_trend': metrics.stability_trend,
                'overall_health': metrics.overall_health
            }
        })
        
        print("=" * 60)
    
    async def generate_analysis_report(self):
        """Generate final comprehensive analysis report"""
        print("\n" + "Status COMPREHENSIVE ANALYSIS REPORT" + "Status")
        print("=" * 80)
        
        # Overall statistics
        print("Summary SUMMARY STATISTICS:")
        if self.analysis_results:
            moving_sessions = sum(1 for r in self.analysis_results if r['is_moving'])
            quality_scores = [r['quality'] for r in self.analysis_results if r['quality']]
            
            print(f"   Total Analysis Cycles: {len(self.analysis_results)}")
            print(f"   Movement Detected: {moving_sessions}/{len(self.analysis_results)} cycles")
            print(f"   Movement Percentage: {(moving_sessions/len(self.analysis_results)*100):.1f}%")
            
            if quality_scores:
                quality_distribution = {}
                for q in quality_scores:
                    quality_distribution[q] = quality_distribution.get(q, 0) + 1
                
                print(f"   Quality Distribution:")
                for quality, count in quality_distribution.items():
                    print(f"     {quality}: {count} times")
        
        # Data collection statistics
        stats = self.data_collector.get_collection_stats()
        print(f"\nData DATA COLLECTION STATS:")
        print(f"   Total Samples: {stats['total_samples']}")
        print(f"   Sampling Rate: {stats['sampling_rate']:.2f} Hz")
        print(f"   Collection Duration: {stats.get('last_sample_time', 0) - stats.get('collection_start_time', 0):.1f}s")
        
        # Final performance analysis
        final_performance = await self.analytics_engine.analyze_recent_performance(60.0)
        if 'error' not in final_performance:
            print(f"\n🏆 FINAL PERFORMANCE ASSESSMENT:")
            metrics = final_performance['performance_metrics']
            print(f"   Overall Smoothness: {metrics['smoothness']['average']:.3f}/1.0")
            print(f"   Overall Efficiency: {metrics['efficiency']['average']:.3f}/1.0")
            print(f"   Overall Stability: {metrics['stability']['average']:.3f}/1.0")
            
            # Calculate overall score
            overall_score = (
                metrics['smoothness']['average'] + 
                metrics['efficiency']['average'] + 
                metrics['stability']['average']
            ) / 3
            
            grade = "A+" if overall_score >= 0.9 else "A" if overall_score >= 0.8 else "B" if overall_score >= 0.7 else "C" if overall_score >= 0.6 else "D"
            print(f"   Target Overall Performance Grade: {grade} ({overall_score:.3f}/1.0)")
        
        # Export data option
        print(f"\nSaving DATA EXPORT:")
        try:
            export_data = await self.data_collector.export_data("json")
            print(f"   Total data points available for export: {len(export_data)}")
            print(f"   Use data_collector.export_data() to get full dataset")
        except Exception as e:
            print(f"   Export preview failed: {e}")
        
        print("=" * 80)
    
    async def cleanup(self):
        """Clean up all resources"""
        print("\nCleaning up...")
        
        if self.analytics_engine:
            await self.analytics_engine.stop_analysis()
        
        if self.stream_processor:
            await self.stream_processor.stop_processing()
        
        if self.data_collector:
            await self.data_collector.stop_collection()
        
        if self.connection:
            await self.connection.disconnect()
        
        print(" Cleanup complete")

async def main():
    """Main function"""
    demo = AdvancedAnalyticsDemo()
    
    # Run demo for 2 minutes (adjust as needed)
    await demo.run_demo(duration_seconds=120)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWARNING  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"FAILED Demo failed: {e}")
        sys.exit(1)
