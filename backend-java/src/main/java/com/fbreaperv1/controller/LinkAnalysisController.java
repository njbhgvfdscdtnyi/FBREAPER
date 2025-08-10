package com.fbreaperv1.controller;

import com.fbreaperv1.service.LinkAnalysisService;
import com.fbreaperv1.model.LinkAnalysisResult;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.HashMap;

@RestController
@RequestMapping("/api/network")
@CrossOrigin(origins = "http://localhost:3000")
public class LinkAnalysisController {

    private final LinkAnalysisService linkAnalysisService;

    public LinkAnalysisController(LinkAnalysisService linkAnalysisService) {
        this.linkAnalysisService = linkAnalysisService;
    }

    @GetMapping("/graph")
    public ResponseEntity<Map<String, Object>> getNetworkGraph(@RequestParam(required = false) String keyword) {
        // Mock network graph data
        Map<String, Object> graphData = new HashMap<>();
        
        // Mock nodes
        Map<String, Object>[] nodes = new Map[5];
        for (int i = 0; i < 5; i++) {
            Map<String, Object> node = new HashMap<>();
            node.put("id", String.valueOf(i + 1));
            node.put("label", "Node " + (i + 1));
            node.put("type", i == 0 ? "group" : "user");
            node.put("connections", (i + 1) * 10);
            nodes[i] = node;
        }
        
        // Mock links
        Map<String, Object>[] links = new Map[4];
        for (int i = 0; i < 4; i++) {
            Map<String, Object> link = new HashMap<>();
            link.put("source", String.valueOf(i + 1));
            link.put("target", String.valueOf(i + 2));
            link.put("strength", 0.5 + (i * 0.1));
            link.put("type", "comment");
            links[i] = link;
        }
        
        graphData.put("nodes", nodes);
        graphData.put("links", links);
        
        return ResponseEntity.ok(graphData);
    }

    @GetMapping("/link-analysis")
    public ResponseEntity<LinkAnalysisResult> analyzeLinks(@RequestParam String url) {
        return ResponseEntity.ok(linkAnalysisService.analyzeLinks(url));
    }
}
